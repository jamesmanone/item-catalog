
let viewModel;

class Item {
  constructor(data) {
    this.name = data.name;
    this.id = data.id;
    this.href = `/item/${this.id}`;
  }
}

class Category {
  constructor(data) {
    this.name = ko.observable(data.name);
    this.id = ko.observable(data.id);
    this.items = ko.observableArray();
  }

  getItems() {
    fetch(`/api/json?method=category.list&q=${this.name()}`)
      .then(res => {
        if(!res.ok) {
          throw new Error('Bad Response');
        } else {
          return res;
        }
      })
      .then(res => res.json())
      .then(res => res.forEach(item => this.items.push(new Item(item))))
      .catch(e => console.error(e));

  }
}

function populateCategoryList() {
  return new Promise((resolve, reject) => {
    let clock = setTimeout(() => reject('Failed to load resources'), 10000);
    fetch('/api/json?method=categories')
      .then(res => res.json())
      .then(res => res.forEach(cat => this.categoryList.push(new Category(cat))))
      .then(() => clearTimeout(clock))
      .then(resolve);
  });
}

function setActiveCategoryFromHash() {
  if(window.location.hash !== '') {
    const hash = window.location.hash.slice(1).replace('%20', ' ').toLowerCase();
    for(let category of this.categoryList()) {
      if (category.name().toLowerCase() === hash) {
        this.listClick(category);
        return;
      }
    }
  }
}

function CategoryListView() {
  // Init
  this.categoryList = ko.observableArray();
  this.activeCategory = ko.observable();

  this.make = populateCategoryList.bind(this);
  this.set = setActiveCategoryFromHash.bind(this);
  this.make().then(this.set).catch(e => {
    const data = {
      name: e,
      id: null
    };
    this.categoryList.push(new Category(data));
  });

  // Category click handler
  this.listClick = cat => {
    this.activeCategory(cat);
    if(!this.activeCategory().items().length) {
      this.activeCategory().getItems();
    }
    const newHash = cat.name().replace(' ', '%20');
    window.location.hash = newHash;
  };
}

ko.applyBindings(new CategoryListView(), document.getElementById('category-view'));
