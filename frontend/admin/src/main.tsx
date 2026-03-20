import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import App from './App.jsx';
import './index.css';

// 模拟Redux store
const store = configureStore({
  reducer: {
    // 添加一个默认的reducer
    app: (state = {}) => state
  },
});

const root = document.getElementById('root');
if (root) {
  ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);
}