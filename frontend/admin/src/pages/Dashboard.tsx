import { Card, Row, Col, Statistic, Table, Progress, Badge, Space, Typography } from 'antd';
import { 
  ShoppingOutlined, 
  UserOutlined
} from '@ant-design/icons';
import { useState, useEffect } from 'react';
import orderService from '../services/orderService';
import customerService from '../services/customerService';
import inventoryService from '../services/inventoryService';
import { Order } from '../types';

const { Title } = Typography;

function Dashboard() {
  const [orderData, setOrderData] = useState<Order[]>([]);
  const [totalSales, setTotalSales] = useState<number>(0);
  const [orderCount, setOrderCount] = useState<number>(0);
  const [inventoryLevel, setInventoryLevel] = useState<number>(0);
  const [customerCount, setCustomerCount] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  
  // 加载仪表盘数据
  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);
        
        // 加载最近订单
        const ordersResponse = await orderService.getOrders({ limit: 4 });
        setOrderData(ordersResponse.data || []);
        
        // 加载总销售额
        // 这里假设API提供了销售额统计
        // 暂时使用模拟数据
        setTotalSales(128000);
        
        // 加载订单数量
        setOrderCount(128);
        
        // 加载库存水平
        const inventoryResponse = await inventoryService.getInventory();
        const inventoryItems = inventoryResponse.data || [];
        if (inventoryItems.length > 0) {
          // 计算平均库存水平
          const totalQuantity = inventoryItems.reduce((sum, item) => sum + item.quantity, 0);
          const totalThreshold = inventoryItems.reduce((sum, item) => sum + item.threshold, 0);
          if (totalThreshold > 0) {
            setInventoryLevel(Math.round((totalQuantity / totalThreshold) * 100));
          }
        }
        
        // 加载客户数量
        const customersResponse = await customerService.getCustomers();
        setCustomerCount(customersResponse.data?.length || 0);
      } catch (error: any) {
        console.error('加载仪表盘数据失败:', error);
      } finally {
        setLoading(false);
      }
    };
    
    loadDashboardData();
  }, []);


  const columns = [
    { title: '订单编号', dataIndex: 'orderId', key: 'orderId' },
    { title: '客户', dataIndex: 'customer', key: 'customer' },
    { title: '金额', dataIndex: 'amount', key: 'amount', render: (text: number) => `¥${text}` },
    { 
      title: '状态', 
      dataIndex: 'status', 
      key: 'status', 
      render: (text: string) => {
        let status: 'success' | 'warning' | 'default' | 'processing' | 'error' = 'default';
        if (text === '已完成') status = 'success';
        if (text === '待支付') status = 'warning';
        return <Badge status={status} text={text} />;
      }
    },
    { title: '日期', dataIndex: 'date', key: 'date' },
  ];

  return (
    <div>
      <Title level={4}>仪表盘</Title>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card loading={loading}>
            <Statistic 
              title="总销售额" 
              value={totalSales} 
              precision={2} 
              styles={{ content: { color: '#3f8600' } }} 
              prefix="¥" 
              suffix="元"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card loading={loading}>
            <Statistic 
              title="订单数量" 
              value={orderCount} 
              styles={{ content: { color: '#1890ff' } }} 
              prefix={<ShoppingOutlined />} 
              suffix="单"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card loading={loading}>
            <Statistic 
              title="库存水平" 
              value={inventoryLevel} 
              styles={{ content: { color: '#faad14' } }} 
              suffix="%"
            />
            <Progress percent={inventoryLevel} status="active" style={{ marginTop: 16 }} />
          </Card>
        </Col>
        <Col span={6}>
          <Card loading={loading}>
            <Statistic 
              title="客户数量" 
              value={customerCount} 
              styles={{ content: { color: '#1890ff' } }} 
              prefix={<UserOutlined />} 
              suffix="个"
            />
          </Card>
        </Col>
      </Row>
      
      <Row gutter={16}>
        <Col span={16}>
          <Card title="最近订单" variant="outlined" loading={loading}>
            <Table dataSource={orderData} columns={columns} pagination={false} />
          </Card>
        </Col>
        <Col span={8}>
          <Card title="销售统计" variant="outlined">
            <Space orientation="vertical" style={{ width: '100%' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span>商品销售</span>
                  <span>¥86,500</span>
                </div>
                <Progress percent={86} status="success" />
              </div>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span>服务销售</span>
                  <span>¥41,500</span>
                </div>
                <Progress percent={42} status="active" />
              </div>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span>其他销售</span>
                  <span>¥12,800</span>
                </div>
                <Progress percent={13} status="normal" />
              </div>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default Dashboard;