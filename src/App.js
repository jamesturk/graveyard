import React from 'react';
import dataBlocks from './data';

class InfoBlock extends React.Component {
  renderAsDefinition() {
    const terms = this.content.data.map(d =>
      <React.Fragment key={d[0]}><dt>{d[0]}</dt><dd>{d[1]}</dd></React.Fragment>);
    return (<dl>{terms}</dl>);
  }

  renderAsTable() {
    let head = '';
    if (this.content.header) {
      head = this.content.header.map(d => <th key={d}>{d}</th>);
    }
    const rows = this.content.data.map(d =>
      <tr key={d[0]}><td>{d[0]}</td><td>{d[1]}</td></tr>);
    return (
      <table>
        <thead><tr>{head}</tr></thead>
        <tbody>{rows}</tbody>
      </table>);
  }

  render() {
    this.content = dataBlocks[this.props.type];
    let inner = '';

    if (this.props.layout === 'definition') {
      inner = this.renderAsDefinition();
    } else {
      inner = this.renderAsTable();
    }

    return (
      <div className="block" id={this.props.type}>
        <h2>{this.props.type}</h2>
        {inner}
      </div>
    );
  }
}

class Page extends React.PureComponent {
  render() {
    const blocks = this.props.blocks.map(b => <InfoBlock type={b} key={b} />);
    return (
      <div className="page sheet">
        {blocks}
      </div>
    );
  }
}

class Controls extends React.PureComponent {
  render() {
    return (
      <div className="controls">
        <button id="addPage" onClick={this.props.addPage}>Add Page</button>
        <button id="removePage" onClick={this.props.removePage}>Remove Page</button>
      </div>
    );
  }
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      pages: [
        ['actions', 'exhaustion'],
        ['lifestyle'],
      ],
    };

    this.addPage = this.addPage.bind(this);
    this.removePage = this.removePage.bind(this);
  }

  addPage() {
    this.state.pages.push([]);
  }

  removePage() {
    this.state.pages.pop();
  }

  render() {
    const pages = this.state.pages.map(p => <Page blocks={p} />);
    return (
      <div className="App">
        <Controls addPage={this.addPage} removePage={this.removePage} />
        {pages}
      </div>
    );
  }
}

export default App;
