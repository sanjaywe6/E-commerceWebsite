$(document).ready(function () {
  $("#cart_cantainer").on("click", ".remove_item", function () {
    id = $(this).attr("data-prod_id");
    operation = $(this).attr("data-operation");
    $.ajax({
      url: "/update_cart/",
      type: "get",
      data: {
        id: id,
        operation: operation,
      },
      success: function (data) {
        status = data.status;
        // if cart update is successful
        if (status == "true") {
          products = data.cart_products;

          // if items in cart is empty
          if (products.length < 1) {
            $("#all_cart_products").html(`<div>
                                        <div class="main_cart_box">
                                            <div class="cart_box">
                                                <div class="cart_data_box">
                                                    <i class="fas fa-tablet-alt" style="font-size: 200px;"></i>
                                                    <div class="my-4">
                                                        <h2 style="display: flex; justify-content:center;"><i class="fas fa-battery-empty mx-3"
                                                                style="color: red; font-size:45px;"></i>Empty Cart</h2>
                                                        <div style="display: flex; justify-content:center;">
                                                            <a href="/" type="button" class="btn btn-danger">Add Items to Cart</a>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>`);
          } else {
            // var adding all products one one by with htm tag
            output = "";
            for (let index = 0; index < products.length; index++) {
              const element = products[index];
              output += `<div style="display: flex; justify-content: center;">
                                                        <div class="card mb-3" style="max-width: 800px; padding: 10px;">
                                                            <div class="row g-0">
                                                                <div class="col-md-4">
                                                                    <img src="/media/${element["product"].image}" class="img-fluid rounded-start" alt="Loading..">
                                                                </div>
                                                                <div class="col-md-8">
                                                                    <div class="card-body">
                                                                        <p class="card-title text-primary h6">${element["product"].title}+</p>
                                                                        <p class="card-text"><b>Price: <i class="fa fa-rupee"></i> ${element["product"].price}</b> </p>
                                                                        <p class="card-text">Quantity <b> ${element["quantity"]} </b> </p>
                                                                        <p class="card-text"><small class="text-body-secondary">Updated on ${element["product"].time}</small></p>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                                                                <button class="btn btn-warning my-2 remove_item" data-prod_id="${element["product"].id}" data-operation="remove"><i class="far fa-trash-alt"></i> Remove from Cart</button>
                                                                <button class="btn btn-danger my-2"><i class="fas fas fa-luggage-cart"></i> Buy Now</button>
                                                            </div>
                                                        </div>
                                                    </div>`;
            }
            $("#all_cart_products").html(output);
          }
        }
      },
    });
  });
});
