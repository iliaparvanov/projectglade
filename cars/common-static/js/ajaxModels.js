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

$("#delete").on('click', function () {
  var user = $("#user").val();
  var pk = $("#pk").val();
  // alert(user);
  // alert(pk);

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

    

