import React, { Component } from 'react';

class DiceTableRow extends Component {
  render() {
    return (
      <tr>
        <td><button name="{this.props.n}" onClick={this.click}>{this.props.n}</button></td>
        <td>{this.props.count}</td>
      </tr>
    );
  }

  click() {
    this.props.count++;
  }
}

class DiceTable extends Component {
  render() {
    var rows = [];
    for(var i=1; i <= this.props.num_sides; i++) {
      rows.push(<DiceTableRow n={i} />);
    }
    return (
      <table>
        <thead>
          <tr><th>#</th><th>count</th></tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    );
  }
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <DiceTable num_sides="6" />
      </div>
    );
  }
}

export default App;
