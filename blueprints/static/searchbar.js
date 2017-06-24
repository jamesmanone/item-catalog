
function SearchbarViewModel() {
  this.query = ko.observable();
  this.searchOptions = ko.observableArray();

  this.query.subscribe(query => {
    if(!query.length) {
      console.log('empty query');
      return;
    }
    fetch('/api/json?method=search&q='+query)
      .then(res => res.json())
      .then(res => {
        this.searchOptions([]);
        res.categories.forEach(catagory => this.searchOptions.push(catagory));
        res.items.forEach(item => this.searchOptions.push(item));
      });
  });
}

ko.applyBindings(new SearchbarViewModel(), document.getElementById('navbar'));
