$(function() {
  $("#search").autocomplete({
    source: "searchService",
    minLength: 2,
  });
});