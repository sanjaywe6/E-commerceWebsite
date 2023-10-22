$(document).ready(function () {
  // function for calling msg
  function show_msg(msg) {
    $("#alert_message").css("display", "unset");
    $("#msg_text").text(msg);
  }
  function hide_msg() {
    $("#alert_message").css("display", "none");
    $("#msg_text").text(msg);
  }

  // js for adding product to cart
  $("#add_to_cart").click(function () {
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
        if (data.status == true) {
          $("#add_to_cart").html(`<i class="fa fa-check"></i>  Added to Cart`);
        }
      },
    });
  });

  // js for submitting comment form
  $("#comment_form").submit(function (e) {
    e.preventDefault();

    // sending comment form post request
    $.ajax({
      url: "/comment/",
      type: "post",
      data: {
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        product_id: $("#product_id").val(),
        comment: $("#input_comment").val(),
      },
      success: function (data) {
        // shownig message returned from server
        show_msg(data.msg);
        console.log(data.comments);
        if (data.status == true) {
          // updating all comments with new comment

          allComment = data.comments;

          output = "";
          for (let index = 0; index < allComment.length; index++) {
            const element = allComment[index];
            output += `
                        <div class="card my-2">
                        <h5 class="card-header"><i class="fas fa-user-alt text-danger"></i>${element.usrname}</h5>
                        <div class="card-body">
                            <p class="card-text">${element.comment}</p>
                        </div>
                        <div class="my-2 mx-2" style="display: flex; justify-content: flex-end;">
                            <small><b>${element.time}</b></small>
                        </div>
                    </div>
                        `;
          }

          $("#all_comments").html(output);
          $("#input_comment").val("");
        }
      },
    });
  });
});
