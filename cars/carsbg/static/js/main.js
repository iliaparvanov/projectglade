// When the user scrolls the page, execute stickToTop
window.onscroll = function() {stickToTop()};

// Get the header
var navbar = document.getElementById("navbar");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function stickToTop() {
  if (window.pageYOffset > sticky) {
    navbar.classList.add("sticky");
  } else {
    navbar.classList.remove("sticky");
  }
}

function stars(num) {
  for(var i = 1; i <= 5; i++)
  {
    var j = (i).toString()

    if(i <= num)
    {
      document.getElementById("star" + j).className = "fa fa-star checked";
    }
    else
    {
      document.getElementById("star" +  j).className = "fa fa-star";
    }
  }
  document.getElementById("rating").value = num;
}

$( function() {
    $.widget( "custom.catcomplete", $.ui.autocomplete, {
      _create: function() {
        this._super;
        this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
      },
      _renderMenu: function( ul, items ) {
        var that = this,
          currentCategory = "";
        $.each( items, function( index, item ) {
          var li;
          if ( item.category != currentCategory ) {
            ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
            currentCategory = item.category;
          }
          li = that._renderItemData( ul, item );
          if ( item.category ) {
            li.attr( "aria-label", item.category + " : " + item.label );
          }
        });
      }
    });
});
$(function() {
  $("#search").catcomplete({
    source: "searchService",
    minLength: 2,
  });
});

var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
}
