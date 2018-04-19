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

// map degrees-of-freedom (sides-1) to 90, 95, 97.5 and 99% thresholds
const CHI_SQUARED_CRITICAL = {
  3: [6.251, 7.815, 9.348, 11.345],
  5: [9.236, 11.070, 12.833, 15.086],
  7: [12.017, 14.067, 16.013, 18.475],
  9: [14.684, 16.919, 19.023, 21.666],
  11: [17.275, 19.675, 21.920, 24.725],
  19: [27.204, 30.144, 32.852, 36.191],
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
      <div>
      <table>
        <thead>
          <tr><th>#</th><th>count</th></tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
      Computed a X<sup>2</sup> of <i>{this.chiSquared()}</i>, probability of bad dice <i>{this.chiSquaredPassage()}</i>
      </div>
    );
  }

  click(i) {
    var newState = this.state;
    newState.counts[i]++;
    this.setState(newState);
  }

  chiSquared() {
    var total = 0;
    for(var i=0; i < this.props.num_sides; i++) {
      total += this.state.counts[i];
    }

    var expected = total / this.props.num_sides;

    var chiSquared = 0;

    for(i=0; i < this.props.num_sides; i++) {
      chiSquared += (this.state.counts[i] - expected) ** 2 / expected;
    }

    return chiSquared;
  }

  chiSquaredPassage() {
    var table = CHI_SQUARED_CRITICAL[this.props.num_sides-1];

    var chiVal = this.chiSquared();

    if(chiVal < table[0]) {
      return '90%';
    } else if(chiVal < table[1]) {
      return '95%';
    } else if(chiVal < table[1]) {
      return '97.5%';
    } else if(chiVal < table[4]) {
      return '99%';
    } else {
      return '100%';
    }
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