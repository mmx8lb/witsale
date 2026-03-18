import { Card, Row, Col, Statistic, List, Typography, Space, Divider } from 'antd'
import { DollarOutlined, ShoppingOutlined, DatabaseOutlined, UserOutlined, BarChartOutlined, ClockCircleOutlined } from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography

const Dashboard = () => {
  // 模拟数据
  const stats = [
    {
      title: '总销售额',
      value: '¥128,500',
      prefix: <DollarOutlined />,
      suffix: '元',
      status: 'up',
      percent: 12,
      color: '#1890ff',
    },
    {
      title: '订单数量',
      value: 328,
      prefix: <ShoppingOutlined />,
      suffix: '单',
      status: 'up',
      percent: 8,
      color: '#52c41a',
    },
    {
      title: '库存总量',
      value: 12580,
      prefix: <DatabaseOutlined />,
      suffix: '件',
      status: 'down',
      percent: 3,
      color: '#faad14',
    },
    {
      title: '客户数量',
      value: 256,
      prefix: <UserOutlined />,
      suffix: '个',
      status: 'up',
      percent: 15,
      color: '#722ed1',
    },
  ]

  const recentOrders = [
    { id: 1, orderNo: 'ORD20260318001', customer: '北京客户A', amount: 5800, status: '已完成' },
    { id: 2, orderNo: 'ORD20260318002', customer: '上海客户B', amount: 3200, status: '处理中' },
    { id: 3, orderNo: 'ORD20260318003', customer: '广州客户C', amount: 8900, status: '已完成' },
    { id: 4, orderNo: 'ORD20260318004', customer: '深圳客户D', amount: 2100, status: '待支付' },
    { id: 5, orderNo: 'ORD20260318005', customer: '成都客户E', amount: 6500, status: '处理中' },
  ]

  return (
    <>
      {/* 页面标题 */}
      <div style={{ marginBottom: '32px' }}>
        <Title level={2} style={{ 
          marginBottom: '8px',
          color: '#333',
          fontWeight: 600
        }}>仪表盘</Title>
        <Paragraph type="secondary" style={{ marginBottom: 0 }}>
          欢迎回来，这里是您的业务概览
        </Paragraph>
      </div>
        
        {/* 统计卡片区域 */}
        <Row gutter={[24, 24]} style={{ marginBottom: '32px' }}>
          {stats.map((stat, index) => (
            <Col 
              key={index} 
              xs={24} 
              sm={12} 
              md={8} 
              lg={6} 
              style={{ display: 'flex' }}
            >
              <Card 
                style={{ 
                  flex: 1, 
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                  borderRadius: '12px',
                  transition: 'all 0.3s ease',
                  border: 'none'
                }}
                hoverable
                bodyStyle={{
                  padding: '24px'
                }}
              >
                <Statistic
                  title={
                    <Text style={{ 
                      fontSize: '14px', 
                      fontWeight: 500,
                      color: '#666'
                    }}>
                      {stat.title}
                    </Text>
                  }
                  value={stat.value}
                  prefix={
                    <span style={{ 
                      color: stat.color,
                      fontSize: '20px'
                    }}>
                      {stat.prefix}
                    </span>
                  }
                  suffix={
                    <Space size={8}>
                      <Text style={{ 
                        fontSize: '12px',
                        color: '#999'
                      }}>
                        {stat.suffix}
                      </Text>
                      <Space size={4} style={{
                        display: 'flex',
                        alignItems: 'center'
                      }}>
                        {stat.status === 'up' ? 
                          <span style={{ 
                            fontSize: '12px', 
                            color: '#52c41a' 
                          }}>↑</span> : 
                          <span style={{ 
                            fontSize: '12px', 
                            color: '#ff4d4f' 
                          }}>↓</span>
                        }
                        <Text 
                          type={stat.status === 'up' ? 'success' : 'danger'} 
                          style={{ 
                            fontSize: '12px',
                            fontWeight: 500
                          }}
                        >
                          {stat.status === 'up' ? '+' : '-'}{stat.percent}%
                        </Text>
                      </Space>
                    </Space>
                  }
                  valueStyle={{ 
                    fontSize: '28px',
                    fontWeight: 600,
                    color: '#333'
                  }}
                />
                <div style={{ 
                  marginTop: '16px',
                  height: '4px',
                  background: '#f0f0f0',
                  borderRadius: '2px',
                  overflow: 'hidden'
                }}>
                  <div 
                    style={{
                      height: '100%',
                      width: `${Math.abs(stat.percent) * 5}%`,
                      background: stat.color,
                      borderRadius: '2px',
                      transition: 'width 0.3s ease'
                    }}
                  />
                </div>
              </Card>
            </Col>
          ))}
        </Row>
        
        <Divider style={{ 
          margin: '40px 0',
          borderColor: '#f0f0f0'
        }} />
        
        {/* 详细数据区域 */}
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={12} style={{ display: 'flex' }}>
            <Card 
              title={
                <Space size={8}>
                  <ClockCircleOutlined style={{ color: '#1890ff' }} />
                  <Text style={{ 
                    fontWeight: 600,
                    fontSize: '16px',
                    color: '#333'
                  }}>最近订单</Text>
                </Space>
              }
              style={{ 
                flex: 1, 
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                borderRadius: '12px',
                border: 'none'
              }}
              bodyStyle={{
                padding: '24px'
              }}
            >
              <List
                dataSource={recentOrders}
                renderItem={(item) => (
                  <List.Item
                    style={{
                      padding: '16px 0',
                      borderBottom: '1px solid #f0f0f0'
                    }}
                  >
                    <List.Item.Meta
                      title={
                        <Space direction="vertical" size={6}>
                          <Text style={{ 
                            fontWeight: 500,
                            color: '#333'
                          }}>
                            {item.orderNo}
                          </Text>
                          <Text style={{ 
                            fontSize: '13px', 
                            color: '#666'
                          }}>
                            {item.customer}
                          </Text>
                        </Space>
                      }
                      description={
                        <Space direction="vertical" size={6}>
                          <Text style={{ 
                            color: '#1890ff',
                            fontWeight: 500,
                            fontSize: '15px'
                          }}>
                            ¥{item.amount}
                          </Text>
                          <Text style={{ 
                            fontSize: '13px',
                            color: 
                              item.status === '已完成' ? '#52c41a' :
                              item.status === '处理中' ? '#faad14' :
                              item.status === '待支付' ? '#ff4d4f' : '#666'
                          }}>
                            {item.status}
                          </Text>
                        </Space>
                      }
                    />
                  </List.Item>
                )}
              />
            </Card>
          </Col>
          <Col xs={24} lg={12} style={{ display: 'flex' }}>
            <Card 
              title={
                <Space size={8}>
                  <BarChartOutlined style={{ color: '#1890ff' }} />
                  <Text style={{ 
                    fontWeight: 600,
                    fontSize: '16px',
                    color: '#333'
                  }}>销售趋势</Text>
                </Space>
              }
              style={{ 
                flex: 1, 
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                borderRadius: '12px',
                border: 'none'
              }}
              bodyStyle={{
                padding: '24px'
              }}
            >
              <div style={{ 
                height: 320, 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                backgroundColor: '#fafafa',
                borderRadius: '8px',
                border: '1px dashed #e8e8e8'
              }}>
                <Text type="secondary">销售趋势图表</Text>
              </div>
            </Card>
          </Col>
        </Row>
    </>
  )
}

export { Dashboard }