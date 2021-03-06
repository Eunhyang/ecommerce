from django.contrib import messages
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

# Create your views here.
from .forms import VariationInventoryFormSet
from .models import Product, Variation
from .mixins import StaffRequiredMixin, LoginRequiredMixin

class VariationListView(LoginRequiredMixin, ListView):

	model = Variation
	#template_name = "<appname>/<modelname>_detail.html"

	def get_context_data(self, *args, **kwargs): #오버라이딩
		context = super(VariationListView, self).get_context_data(*args, **kwargs)
		context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
		# print context
		return context

	def get_queryset(self, *args, **kwargs): #오버라이딩\
		product_pk = self.kwargs.get('pk') #self.kwargs = {'pk':'pk값'}
		product = get_object_or_404(Product, pk=product_pk)
		queryset = product.variation_set.all()
		return queryset

	def post(self, request ,*args, **kwargs):
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		print(request.POST)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False) # 기존의 form + 새로운 form 저장하기위해(product값 필요) 아래와 같이 처리
				if new_item.title:
					product_pk = self.kwargs.get('pk') 
					product = get_object_or_404(Product, pk=product_pk)
					new_item.product = product
					new_item.save()
			messages.success(request, "inventory update 성공!")
			return redirect("products")
		raise Http404


class ProductListView(ListView):

	model = Product
	query_set = Product.objects.all()
	template_name = "products/product_list.html"

	def get_context_data(self, *args, **kwargs): #오버라이딩
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		# print context
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query) |
				Q(price=query)
				)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs


class ProductDetailView(DetailView):

	model = Product
	#template_name = "<appname>/<modelname>_detail.html"

def product_detail_view_func(request,id):

	product_instance = Product.objects.get(id=id)
	template = "products/product_detail.html"
	context = {
		"object" : product_instance
	}

	return render(request, template, context)
