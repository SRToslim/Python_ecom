$(document).ready(function(){
    // Review
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    $('#commentForm').submit(function(e) {
        e.preventDefault();

        let dt = new Date();
        let time = dt.getDay() + ' ' + monthNames[dt.getUTCMonth()] + ', ' + dt.getFullYear()

        $.ajax({
            method: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function(res){
                if(res.bool == true){
                    $('#addReview').html('Review added successfully.')
                    $('#commentForm').hide()
                    $('#hrv').hide()

                    let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="'+ res.context.image +'" alt="" /><br>'
                    _html += '</div>'
                    _html += '<div class="desc">'

                    if (res.context.fullName != null) {
                        _html += '<p class="font-heading text-brand">' + res.context.fullName + '</p>';
                    } else {
                        _html += '<p class="font-heading text-brand">' + res.context.user + '</p>';
                    }

                    _html += '<div class="d-flex mb-10">'

                    for(let i = 1; i <= res.context.rating; i++){
                        _html += '<div class="text-end">'
                        _html += '<i class="fas fa-star text-warning"></i>'
                        _html += '</div>'
                    }

                    _html += '</div>'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">'+ time +'</span>'
                    _html += '</div>'
                    _html += '<p class="mb-10">'+ res.context.review +'</p>'
                    _html += '</div>'
                    _html += '</div>'

                    $('.comment-list').prepend(_html)
                }
            },
        })
    });


    // Clock
    function updateClock() {
        const now = new Date();
        const clockElement = document.getElementById("clock");
        clockElement.innerHTML = now.toLocaleTimeString();
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Product Filter
	$('.filter-checkbox, #price-filter-btn').on('click', function(){
		let filter_object = {}

        let min_price = $('#max_price').attr('min')
        let max_price = $('#max_price').val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

		$('.filter-checkbox').each(function(){
			let filter_velue = $(this).val()
			let filter_key = $(this).data('filter')
			// console.log(filter_velue, filter_key);
			filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+filter_key+']:checked')).map(function(e){
                return e.value
            })
		})
		console.log(filter_object);
		$.ajax({
			url: '/filter-products',
			data: filter_object,
			dataType: 'json',
			success: function(response){
				$('#filteredProduct').html(response.data)
			}
		})
	})

    // Price Filter
    $('#max_price').on('blur', function(){
        let min_price = $(this).attr('min')
        let max_price = $(this).attr('max')
        let current_price = $(this).val()

        if(current_price < parseInt(min_price) || current_price > parseInt(mix_price)){

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            alert('Price must between ৳'+min_price + ' ' + 'and' + ' ৳' +max_price)
            $(this).val(min_price)
            $('#range').val(min)
            $(this).focus()

            return false
        }
    })

    // Add to cart
    $('.add-to-cart-btn').on('click', function(){
        let this_val = $(this)
        let index = this_val.attr('data-index')
        let id = $('.product-id-'+index).val()
        let slug = $('.product-slug-'+index).val()
        let name = $('.product-name-'+index).val()
        let image = $('.product-image-'+index).val()
        let quantity = $('.product-qty-'+index).val()
        let sku = $('.product-sku-'+index).val()
        let tax = $('.product-tax-'+index).val()
        let price = $('.product-price-'+index).val()

        $.ajax({
            url:'/add-to-cart',
            data:{
                'id' : id,
                'slug' : slug,
                'image' : image,
                'name': name,
                'qty' : quantity,
                'price' : price,
                'sku' : sku,
                'tax' : tax,
            },
            dataType:'json',
            beforeSend: function(){
                this_val.html('✔')
            },
            success: function(response){
                this_val.html('✔')
                $('.cart-items-count').text(response.totalcartitems)
            }
        })
    })

    // Cart Item Delete
    $('.delete-item').on('click', function(){
        let product_id = $(this).attr('data-item')
        let this_val = $(this)

        $.ajax({
            url:'/delete-from-cart',
            data:{
                'id':product_id,
            },
            dataType:'json',
            beforeSend:function(){
                this_val.attr('disabled',true);
            },
            success:function(res){
                $('.cart-item-count').text(res.totalcartitems)
                this_val.attr('disabled',false);
                $('#cartList').html(res.data)
            }
        });
    })

    // Cart Item Update
    $('.update-item').on('click', function(){
        let product_id = $(this).attr('data-item')
        let product_qty = $('.product-qty-'+product_id).val()
        let this_val = $(this)

        $.ajax({
            url:'/update-cart-item',
            data:{
                'id':product_id,
                'qty':product_qty,
            },
            dataType:'json',
            beforeSend:function(){
                this_val.attr('disabled',true);
            },
            success:function(res){
                $('.cart-item-count').text(res.totalcartitems)
                this_val.attr('disabled',false);
                $('#cartList').html(res.data)
            }
        });
    })

    // Password Show/Hide
    $('.pass_show').append('<span class="ptxt">Show</span>');

    $(document).on('click','.pass_show .ptxt', function(){
        $(this).text($(this).text() == "Show" ? "Hide" : "Show");
        $(this).prev().attr('type', function(index, attr){return attr == 'password' ? 'text' : 'password'; });
    });

    // Message Hide
    setTimeout(() =>{
        $('.alert').alert('close')
    }, 5000)

    // Country Select
    $("#country").countrySelect({
        defaultStyling:"inside",
        defaultCountry:"bd",
        preferredCountries: ['bd'],
    });
});


