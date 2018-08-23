$("#brandId").change(function () {
  var brand = $(this).val();

  $.ajax({
    url: '/ajax/displayModels/',
    data: {
      'brand': brand
    },
    dataType: 'json',
    
  }).then(function(responce){
        response=toJSON(response);
         
        var select = document.getElementById("model"),
        for (var model in response) {
            opt = document.createElement("option");
            opt.value = model.name;
            opt.textContent = model.name;
            select.appendChild(opt);
    }
});
    

