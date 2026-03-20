import { useState } from 'react';
import { Layout, Menu, Button, Avatar, Dropdown, Space, Badge, theme, Drawer } from 'antd';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { 
  DashboardOutlined, 
  ProductOutlined, 
  ShoppingOutlined, 
  InboxOutlined, 
  UserOutlined, 
  CreditCardOutlined, 

  BellOutlined,
  SettingOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  MenuOutlined
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;
const { useToken } = theme;

function MainLayout() {
  const location = useLocation();
  const { token } = useToken();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  const toggleCollapse = () => {
    setCollapsed(!collapsed);
  };
  
  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };
  
  const menuItems = [
    {
      key: '1',
      icon: <DashboardOutlined />,
      label: <Link to="/">仪表盘</Link>,
    },
    {
      key: '2',
      icon: <ProductOutlined />,
      label: <Link to="/products">商品管理</Link>,
    },
    {
      key: '3',
      icon: <ShoppingOutlined />,
      label: <Link to="/orders">订单管理</Link>,
    },
    {
      key: '4',
      icon: <InboxOutlined />,
      label: <Link to="/inventory">库存管理</Link>,
    },
    {
      key: '5',
      icon: <UserOutlined />,
      label: <Link to="/customers">客户管理</Link>,
    },
    {
      key: '6',
      icon: <CreditCardOutlined />,
      label: <Link to="/finance">财务管理</Link>,
    },
  ];

  const userMenu = [
    {
      key: 'profile',
      label: '个人中心',
    },
    {
      key: 'settings',
      label: '设置',
    },
    {
      key: 'logout',
      label: '退出登录',
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh', width: '100%' }}>
      {/* 桌面端侧边栏 */}
      <Sider 
        theme="dark" 
        width={240} 
        collapsedWidth={80}
        collapsed={collapsed}
        style={{ 
          background: token.colorBgContainer, 
          position: 'fixed',
          left: 0,
          top: 0,
          height: '100vh',
          zIndex: 10
        }}
        trigger={null}
      >
        <div className="logo" style={{ 
          height: 64, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          fontSize: 18, 
          fontWeight: 'bold', 
          color: '#fff',
          transition: 'all 0.3s'
        }}>
          {!collapsed && 'Witsale 管理系统'}
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname.split('/')[1] || '1']}
          items={menuItems}
          style={{ height: '100%', borderRight: 0 }}
        />
      </Sider>
      
      {/* 移动端侧边抽屉 */}
      <Drawer
        title="Witsale 管理系统"
        placement="left"
        onClose={toggleMobileMenu}
        open={mobileMenuOpen}
        styles={{ body: { padding: 0 } }}
        size={240}
      >
        <Menu
          mode="inline"
          selectedKeys={[location.pathname.split('/')[1] || '1']}
          items={menuItems}
          style={{ height: '100%', borderRight: 0 }}
          onClick={toggleMobileMenu}
        />
      </Drawer>
      
      {/* 主内容区域 */}
      <Layout style={{ 
        marginLeft: collapsed ? 80 : 240,
        transition: 'margin-left 0.3s',
        minHeight: '100vh'
      }}>
        <Header style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between', 
          padding: '0 24px', 
          background: token.colorBgContainer, 
          boxShadow: token.boxShadow, 
          position: 'fixed',
          top: 0,
          left: collapsed ? 80 : 240,
          right: 0,
          zIndex: 9,
          height: 64,
          transition: 'left 0.3s'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <Button 
              type="text" 
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} 
              onClick={toggleCollapse}
              style={{ fontSize: 16, width: 32, height: 32 }}
            />
            <Button 
              type="text" 
              icon={<MenuOutlined />} 
              onClick={toggleMobileMenu}
              style={{ fontSize: 16, width: 32, height: 32, display: 'none' }}
              className="mobile-menu-button"
            />
            <div style={{ fontSize: 16, fontWeight: 'bold' }}>欢迎使用 Witsale 管理系统</div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <Badge count={5} showZero>
              <Button type="text" icon={<BellOutlined />} />
            </Badge>
            <Button type="text" icon={<SettingOutlined />} />
            <Dropdown menu={{ items: userMenu }}>
              <Space>
                <Avatar size="small" icon={<UserOutlined />} />
                <span>管理员</span>
              </Space>
            </Dropdown>
          </div>
        </Header>
        <Content style={{ 
          margin: '88px 24px 24px', 
          padding: 24, 
          background: token.colorBgContainer, 
          borderRadius: token.borderRadiusLG, 
          minHeight: 280,
          overflow: 'auto'
        }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}

export default MainLayout;