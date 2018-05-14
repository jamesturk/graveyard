import React, { Component } from 'react';
import './App.css';
import dataBlocks from './data.js';

class InfoBlock extends Component {
  render() {
    let data = dataBlocks[this.props.type].data;
    let inner = '';

    if(this.props.layout === 'definition') {
      inner = this.renderAsDefinition(data);
    } else {
      inner = this.renderAsTable(data);
    }

    return (
      <div className="block" id={this.id}>
        <h2>{this.title}</h2>
        {inner}
      </div>
    );
  }

  renderAsDefinition(data) {
    const terms = data.map(
      (d, i) => <React.Fragment key={i}><dt>{d[0]}</dt><dd>{d[1]}</dd></React.Fragment>
    );
    return (<dl>{terms}</dl>);
  }

  renderAsTable(data) {
    const head = ['one', 'two'].map(
      (d, i) => <th key={i}>{d}</th>
    );
    const rows = data.map(
      (d, i) => <tr key={i}><td>{d[0]}</td><td>{d[1]}</td></tr>
    );
    return (<table>
      <thead><tr>
        {head}
      </tr></thead>
      <tbody>
      {rows}
      </tbody>
    </table>);
  }
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <InfoBlock type="actions" />
        <InfoBlock type="exhaustion" layout="definition" />
      </div>
    );
  }
}

export default App;