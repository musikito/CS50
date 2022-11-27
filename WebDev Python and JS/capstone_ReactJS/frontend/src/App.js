import React from "react";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';

class App extends React.Component {

  state = {
    genre_detalles: [],

  };

  componentDidMount() {
    let data;

    axios
      .get('http://localhost:8000/api/musican/')
      .then((res) => {
        data = res.data;
        console.log(data);
        this.setState({
          genre_detalles: data,
        });
      })
      .catch((err) => { });

  } // End of componentDidMount



  render() {
    return (
      <div>
        {this.state.genre_detalles.map((detalles, id) => (
          <div key={id}>
            <h1>{detalles.genre_name}</h1>
          </div>
        ))}
      </div>
    );
  } // End of render
} // End of App
export default App;
