def create_order(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'store/order_form.html', {'product': product})

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)