$("#brandsId").change(function () {
  var brand = $(this).val();

  $.ajax({
    url: 'ajax/displayModels/',
    data: {
      'brand': brand
    },
    dataType: 'json',
    success: function (response, status) {
         
            var select = document.getElementById("modelsId");
            var length = select.options.length;
            $(select).children('option').remove();

            opt = document.createElement("option");
            opt.value = "Всички";
            opt.textContent = "Всички";
            select.appendChild(opt);
            for (model in response.models) 
            {
                opt = document.createElement("option");
                opt.value = response.models[model];
                opt.textContent = response.models[model];
                select.appendChild(opt);
            }
        },
  })
});

$("#addComment").on('click', function () {
  var comment = $("#comment").val();
  if (!$("#addCommentForm")[0].checkValidity()) {
     $("#addCommentForm").find("#hiddenBtn").click();
     return;
  }
  var user = $("#user").val();
  var typeOfObject = $("#typeOfObject").val();
  var pk = $("#pk").val();
  var rating = $("#rating").val();

  $.ajax({
    url: '/ajax/addComment/',
    data: {
      'comment' : comment,
      'user' : user,
      'pk' : pk,
      'typeOfObject' : typeOfObject,
      'rating' : rating,

    },
    dataType: 'json',
    success: function (response, status) {
            if (response.alert != "")
            {
              alertField = document.getElementById("alert")
              alertField.text = response.alert
              alertField.className = "alert alert-danger"
            }
            else 
            {
              location.reload();

            }
            
        
    },
  })
});

$("#delete").on('click', function () {
  var user = $("#user").val();
  var pk = $("#pk").val();

  $.ajax({
    url: '/ajax/deleteComment/',
    data: {
      'user' : user,
      'pk' : pk,
    },
    dataType: 'json',
    success: function (response, status) {
         
            location.reload();
        },
  })
});

    

