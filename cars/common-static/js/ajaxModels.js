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
            for (model in response.models) 
            {
                opt = document.createElement("option");
                opt.value = response.models[model];
                opt.textContent = response.models[model];
                select.appendChild(opt);
            }
        },
    
  })
  // .then(function(responce)
  // {
  //       response=toJSON(response);
         
  //       var select = document.getElementById("modelsId");
  //       for (var model in response) 
  //       {
  //           opt = document.createElement("option");
  //           opt.value = model.name;
  //           opt.textContent = model.name;
  //           select.appendChild(opt);
  //       }
  //  });     
});

    

