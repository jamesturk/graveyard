import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import DicePicker from './DicePicker';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<DicePicker />, document.getElementById('root'));
registerServiceWorker();
