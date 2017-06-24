
function SearchViewModel() {
  this.query = ko.observable();
  this.options = ko.observableArray();

  this.query.subscribe(query => {
    fetch('/api/json?method=search&q='+query)
      .then(res => res.json())
      .then(res => {
        this.options([]);
        if(query.length){
          res.categories.forEach(category => this.options.push(category));
          res.items.forEach(item => this.options.push(item));
        }
    });
  });
}

ko.applyBindings(new SearchViewModel(), document.getElementById('search-page'));
