import React, { Component } from 'react';

class DiceTableRow extends Component {
  render() {
    return (
      <tr>
        <td><button name="{this.props.n}" onClick={this.props.click}>{this.props.n}</button></td>
        <td>{this.props.count}</td>
      </tr>
    );
  }
}

class DiceTable extends Component {
  constructor(props) {
    super(props);
    var counts = [];

    for(var i=0; i < this.props.num_sides; i++) {
      counts.push(0);
    }

    this.state = {'counts': counts};
  }

  renderRow(i) {
    return (<DiceTableRow n={i} count={this.state.counts[i]} click={() => this.click(i)} key={i} />);
  }

  render() {
    var rows = [];
    for(var i=0; i < this.props.num_sides; i++) {
      rows.push(this.renderRow(i));
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

  click(i) {
    var newState = this.state;
    newState.counts[i]++;
    this.setState(newState);
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