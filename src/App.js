import React, { Component } from 'react';
import './App.css';
import dataBlocks from './data.js';

class InfoBlock extends Component {
  render() {
    let content = dataBlocks[this.props.type];
    let inner = '';

    if(this.props.layout === 'definition') {
      inner = this.renderAsDefinition(content);
    } else {
      inner = this.renderAsTable(content);
    }

    return (
      <div className="block" id={this.props.type}>
        <h2>{this.props.type}</h2>
        {inner}
      </div>
    );
  }

  renderAsDefinition(content) {
    const terms = content.data.map(
      (d, i) => <React.Fragment key={i}><dt>{d[0]}</dt><dd>{d[1]}</dd></React.Fragment>
    );
    return (<dl>{terms}</dl>);
  }

  renderAsTable(content) {
    const head = (content.header || ["", ""]).map(
      (d, i) => <th key={i}>{d}</th>
    );
    const rows = content.data.map(
      (d, i) => <tr key={i}><td>{d[0]}</td><td>{d[1]}</td></tr>
    );
    return (<table>
      <thead><tr>{head}</tr></thead>
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
        <InfoBlock type="exhaustion" />
      </div>
    );
  }
}

export default App;