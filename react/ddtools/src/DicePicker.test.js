import React from 'react';
import ReactDOM from 'react-dom';
import DicePicker from './App';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<DicePicker />, div);
  ReactDOM.unmountComponentAtNode(div);
});
