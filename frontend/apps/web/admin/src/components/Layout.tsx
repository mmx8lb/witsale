import { useState, useEffect } from 'react'
import { Outlet, Link, useNavigate } from 'react-router-dom'
import { Layout, Menu, Button, Dropdown, Space, ConfigProvider } from 'antd'
import { LogoutOutlined, UserOutlined, DashboardOutlined, ProductOutlined, ShoppingOutlined, DatabaseOutlined, UsergroupAddOutlined, DollarOutlined, FieldTimeOutlined, LineChartOutlined, MenuFoldOutlined, MenuUnfoldOutlined } from '@ant-design/icons'
import { useDispatch, useSelector } from 'react-redux'
import { logout } from '@/store/authSlice'

const { Header, Sider, Content } = Layout

const LayoutComponent = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const { user } = useSelector((state: any) => state.auth)
  const [collapsed, setCollapsed] = useState(false)
  const [isMobile, setIsMobile] = useState(false)

  // 检测屏幕尺寸变化
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768)
    }

    // 初始检测
    handleResize()
    
    // 添加 resize 事件监听器
    window.addEventListener('resize', handleResize)
    
    // 清理事件监听器
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const handleLogout = async () => {
    dispatch(logout() as any)
    navigate('/login')
  }

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
      icon: <DatabaseOutlined />,
      label: <Link to="/inventory">库存管理</Link>,
    },
    {
      key: '5',
      icon: <UsergroupAddOutlined />,
      label: <Link to="/customers">客户管理</Link>,
    },
    {
      key: '6',
      icon: <DollarOutlined />,
      label: <Link to="/finance">财务管理</Link>,
    },
    {
      key: '7',
      icon: <FieldTimeOutlined />,
      label: <Link to="/field-service">外勤管理</Link>,
    },
    {
      key: '8',
      icon: <LineChartOutlined />,
      label: <Link to="/knowledge-graph">知识图谱</Link>,
    },
  ]

  const userMenu = [
    {
      key: 'profile',
      label: '个人信息',
    },
    {
      key: 'settings',
      label: '设置',
    },
    {
      key: 'logout',
      label: (
        <Button type="text" danger icon={<LogoutOutlined />} onClick={handleLogout}>
          退出登录
        </Button>
      ),
    },
  ]

  return (
    <ConfigProvider>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider 
          collapsible 
          collapsed={collapsed} 
          onCollapse={(value) => setCollapsed(value)}
          breakpoint="lg"
          collapsedWidth={isMobile ? 0 : 80}
          width={240}
          style={{
            background: 'linear-gradient(135deg, #1890ff 0%, #096dd9 100%)',
            boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)',
          }}
        >
          <div className="logo" style={{ 
            height: '64px', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            color: '#fff', 
            fontSize: '18px', 
            fontWeight: 'bold',
            padding: '0 16px',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap'
          }}>
            {!collapsed || isMobile ? 'Witsale 管理端' : 'Witsale'}
          </div>
          <Menu 
            theme="dark" 
            mode="inline" 
            defaultSelectedKeys={['1']} 
            items={menuItems}
            style={{
              background: 'transparent',
              borderRight: 'none',
            }}
            className="sidebar-menu"
          />
        </Sider>
        <Layout className="site-layout" style={{ transition: 'all 0.3s ease' }}>
          <Header 
            className="site-layout-background" 
            style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between',
              padding: '0 24px',
              height: 64,
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
              background: '#fff',
              position: 'sticky',
              top: 0,
              zIndex: 100
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
              <Button 
                type="text" 
                icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} 
                onClick={() => setCollapsed(!collapsed)}
                style={{ fontSize: '16px' }}
              />
              <div style={{ 
                fontSize: '16px', 
                fontWeight: '500',
                color: '#1890ff'
              }}>
                {user?.username || '管理员'}
              </div>
            </div>
            <Dropdown menu={{ items: userMenu }} placement="bottomRight">
              <Button 
                type="default" 
                icon={<UserOutlined />} 
                style={{ 
                  borderColor: '#d9d9d9', 
                  color: '#666',
                  borderRadius: '4px'
                }}
              >
                <Space size={8}>
                  {user?.username || '管理员'}
                </Space>
              </Button>
            </Dropdown>
          </Header>
          <Content 
            style={{ 
              margin: '24px', 
              padding: '24px', 
              background: '#fff',
              minHeight: 280,
              borderRadius: '8px',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
            }}
          >
            <Outlet />
          </Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  )
}

export { LayoutComponent as Layout }