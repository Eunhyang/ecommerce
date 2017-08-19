from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.
class ProductQuerySet(models.query.QuerySet):
	def activate(self):
		return self.filter(activate = True)

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_queryset().activate()
		


class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	activate = models.BooleanField(default=True)
	#slug
	#inventory?

	objects = ProductManager()

	def __str__(self):
		return self.title
		
	def get_absolute_url(self):
		return reverse("product_detail", kwargs={"pk": self.pk})


class Variation(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	activate = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.title		

	def get_price(self):
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price

	def get_absolute_url(self):
		self.product.get_absolute_url() #프로덕트의 url이 필오할 수 있다

@receiver( post_save, sender = Product )
def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
	product = instance
	variations = product.variation_set.all()

	if variations.count() == 0:
		new_var = Variation()
		new_var.title = "Default"
		new_var.product = product
		new_var.price = product.price
		new_var.save()

# post_save.connect(product_post_saved_receiver, sender=Product)

def image_upload_to(instance, filename):
	title = instance.product.title
	slug = slugify(title)

	#filename을 slug-instance_id.확장명(jpg,png)
	basename, file_extension = filename.split(".")# file_extension에 확장명을 담음
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "products/%s/%s" %(slug,new_filename)

class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to=image_upload_to)

	def __str__(self):
		return self.product.title




