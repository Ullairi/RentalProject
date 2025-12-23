from django.db import models
from django.utils import timezone


class TimestampMixin(models.Model):
    """Custom mixin to add created_at and updated_at fields"""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Update date'
    )

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """Custom Queryset for filtering of deleted records"""
    def delete(self):
        """Soft delete for all Queryset"""
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        """Hard delete for all Queryset"""
        return super().delete()

    def show_not_deleted(self):
        """Only not deleted records"""
        return self.filter(deleted_at__isnull=True)

    def show_deleted(self):
        """Only deleted records"""
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    """Custom Manager that returns only not deleted records"""
    def get_queryset(self):
        """
        This function overrides def. queryset to show only not deleted records
        """
        return SoftDeleteQuerySet(self.model, using=self._db).show_not_deleted()

    def all_records(self):
        """All records including deleted and non-deleted"""
        return SoftDeleteQuerySet(self.model, using=self._db)

    def deleted_only(self):
        """Only deleted records"""
        return SoftDeleteQuerySet(self.model, using=self._db).show_deleted()


class SoftDeleteMixin(models.Model):
    """
    Custom mixin for soft deletion
    (e.g. Records will be marked as deleted, instead of full deletion from DB.
    Records still will be saved in DB for restoration, history, statistic etc. )
    """
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Deletion date'
    )

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft deletion of record(simply mark record as deleted)"""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        """Restoration of deleted record"""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    def hard_delete(self):
        """Hard deletion of record(from database)"""
        super().delete()
