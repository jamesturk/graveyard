import React, { Component } from 'react';

// map degrees-of-freedom (sides-1) to 90, 95, 97.5 and 99% thresholds
const CHI_SQUARED_CRITICAL = {
  3: [6.251, 7.815, 9.348, 11.345],
  5: [9.236, 11.070, 12.833, 15.086],
  7: [12.017, 14.067, 16.013, 18.475],
  9: [14.684, 16.919, 19.023, 21.666],
  11: [17.275, 19.675, 21.920, 24.725],
  19: [27.204, 30.144, 32.852, 36.191],
}

class DiceTableRow extends Component {
  render() {
    return (
      <tr>
        <td><button name="{this.props.n}" onClick={this.props.click}>{this.props.n+1}</button></td>
        <td>{this.props.count}</td>
      </tr>
    );
  }
}

class DiceTable extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  static getDerivedStateFromProps(nextProps, prevState) {
    var counts = Array(parseInt(nextProps.numSides)).fill(0);
    return {'counts': counts};
  }

  renderRow(i) {
    return (<DiceTableRow n={i} count={this.state.counts[i]} click={() => this.click(i)} key={i} />);
  }

  render() {
    var rows = [];
    for(var i=0; i < this.props.numSides; i++) {
      rows.push(this.renderRow(i));
    }
    return (
      <div>
      <table>
        <thead>
          <tr><th>#</th><th>count</th></tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
      Computed a <i>X</i><sup>2</sup> of <i>{this.chiSquared().toFixed(2)}</i>, probability of bad dice <i>{this.chiSquaredPassage()}</i>
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
    var chiSquared = 0;

    for(var count of this.state.counts) {
      total += count;
    }
    var expected = total / this.props.numSides;

    for(count of this.state.counts) {
      chiSquared += (count - expected) ** 2 / expected;
    }

    return chiSquared;
  }

  chiSquaredPassage() {
    var table = CHI_SQUARED_CRITICAL[this.props.numSides-1];

    var chiVal = this.chiSquared();

    if(chiVal < table[0]) {
      return '<90%';
    } else if(chiVal < table[1]) {
      return '90-95%';
    } else if(chiVal < table[2]) {
      return '95-97.5%';
    } else if(chiVal < table[3]) {
      return '97.5-99%';
    } else {
      return '>99%';
    }
  }
}

class DicePicker extends Component {
  constructor(props) {
    super(props);

    this.state = {numSides: "4"};

    this.onChange = this.onChange.bind(this);
  }

  render() {
    var numbers = ['4', '6', '8', '10', '12', '20'];
    var options = [];

    for(var n of numbers) {
      options.push(
        <React.Fragment key={n}>
          <input type="radio" name="numSides" value={n} id={'ns' + n}
           checked={this.state.numSides === n} onChange={this.onChange} />
          <label htmlFor={'ns' + n}>d{n}</label>
        </React.Fragment>
        );
    }

    return (
      <div className="dicePicker">
        {options}

        <DiceTable numSides={this.state.numSides} />
      </div>
    )
  }

  onChange(e) { 
    this.setState({numSides: e.target.value});
  }
}

export default DicePicker;