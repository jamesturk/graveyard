import React, { Component } from 'react';
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
      <tbody>{rows}</tbody>
    </table>);
  }
}

class Page extends Component {
  render() {
    const blocks = this.props.blocks.map((b, i) => <InfoBlock type={b} key={i} />);
    return (
      <div className="page sheet">
        {blocks}
      </div>
    )
  }
}

class Controls extends Component {
  render() {
    return (
      <div className="controls">
        <button id="addPage" onClick={this.props.addPage}>Add Page</button>
        <button id="removePage" onClick={this.props.removePage}>Remove Page</button>
      </div>
    )
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      pages: [
        ['actions', 'exhaustion'],
        ['lifestyle'],
      ]
    };
    
    this.addPage = this.addPage.bind(this);
    this.removePage = this.removePage.bind(this);
  }

  render() {
    const pages = this.state.pages.map((p, i) => <Page blocks={p} key={i} />);
    return (
      <div className="App">
        <Controls addPage={this.addPage} removePage={this.removePage} />
        {pages}
      </div>
    );
  }

  addPage() {
    this.state.pages.push([]);
  }

  removePage() {
    this.state.pages.pop();
  }
}

export default App;