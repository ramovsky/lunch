var restaurants = [
  {name: "Sisaket", distance: .6},
  {name: "Lyly", distance: .8},
];

var RestaurantsBox = React.createClass({
  loadRestaurants: function(){
    $.ajax({
      url: '/restaurants/',
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({restaurants: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  addRestaurant: function(data){
    $.ajax({
      method: 'post',
      data: JSON.stringify(data),
      url: '/restaurants/',
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({restaurants: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  deleteRestaurant: function(data){
    $.ajax({
      method: 'delete',
      data: JSON.stringify(data),
      url: '/restaurants/',
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({restaurants: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function(){
    return {restaurants: []};
  },
  componentDidMount: function() {
    this.loadRestaurants();
    setInterval(this.loadRestaurants, 2000);
  },
  render: function(){
    return (
      <div className="restaurants">
      <h2>Restaurant name and distance</h2>
      <RestaurantList data={this.state.restaurants} deleteRestaurant={this.deleteRestaurant}/>
      <AddNew addRestaurant={this.addRestaurant}/>
      </div>
    );
  }
});

var RestaurantList = React.createClass({
  render: function(){
    var {data, ...other} = this.props
    var restaurant_node = data.map(function(restaurant, i){
      return (
	<Restaurant name={restaurant.name} distance={restaurant.distance} {...other}/>
      );
    }.bind(this));
    return (
      <table className="restaurant_list">
      {restaurant_node}
      </table>
    );
  }
});

var Restaurant = React.createClass({
  handleDelete: function(e) {
    this.props.deleteRestaurant({name: this.props.name});
  },
  render: function(){
    return (
      <tr className="restaurant">
      <td className="restaurant_name">{this.props.name}</td>
      <td>{this.props.distance}</td>
      <td><a onClick={this.handleDelete}>Delete</a></td>
      </tr>
    );
  }
});

var AddNew = React.createClass({
  getInitialState: function() {
    return {name: '', distance: 0.5};
  },
  handleNameChange: function(e) {
    this.setState({name: e.target.value});
  },
  handleDistanceChange: function(e) {
    this.setState({distance: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var name = this.state.name.trim();
    var distance = this.state.distance;
    if (!name || !distance) {
      return;
    }
    this.props.addRestaurant(this.state);
    this.setState({name: '', distance: 0.5});
  },
  render: function(){
    return (
      <form className="add_restaurant_form" onSubmit={this.handleSubmit}>
      <input
      type="text"
      placeholder="Restaurant name"
      className="restaurant_name"
      value={this.state.name}
      onChange={this.handleNameChange}/>
      <input
      type="text"
      className="restaurant_distance"
      value={this.state.distance}
      onChange={this.handleDistanceChange}/>
      <input type="submit" value="Add"/>
      </form>
    );
  }
});

ReactDOM.render(
  <RestaurantsBox />,
  document.getElementById('content')
);

window.data = restaurants
