// 导入Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
// 导入Bootstrap JS
import * as bootstrap from 'bootstrap';

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function () {
  // 初始化Bootstrap组件
  const tooltipTriggerList = document.querySelectorAll(
    '[data-bs-toggle="tooltip"]'
  );
  const tooltipList = [...tooltipTriggerList].map(
    (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
  );

  // 初始化下拉菜单
  const dropdownTriggerList = document.querySelectorAll(
    '[data-bs-toggle="dropdown"]'
  );
  const dropdownList = [...dropdownTriggerList].map(
    (dropdownTriggerEl) => new bootstrap.Dropdown(dropdownTriggerEl)
  );

  // 初始化模态框
  const modalTriggerList = document.querySelectorAll(
    '[data-bs-toggle="modal"]'
  );
  const modalList = [...modalTriggerList].map(
    (modalTriggerEl) => new bootstrap.Modal(modalTriggerEl)
  );

  console.log('Witsale 企业门户初始化完成');
});
