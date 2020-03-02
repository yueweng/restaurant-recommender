Restaurants = {
  init: function(restaurant_names) {
    this.tableSorter();
    this.autoComplete(restaurant_names)
  },

  tableSorter: function() {
    $("#restaurants-table").tablesorter({ sortList: [[0, 0, 0, 1, 0, 0]] });
  },

  autoComplete: function(restaurant_names) {
    $(".input-text.restaurant" ).autocomplete({
      source: restaurant_names
    });
  }
}