import { Card, Table, Button, Space, Input, Select, Typography, message, Modal, Badge, DatePicker } from 'antd';
import { 
  EditOutlined, 
  DeleteOutlined, 
  SearchOutlined,
  EyeOutlined
} from '@ant-design/icons';
import { useState, useEffect } from 'react';
import orderService from '../services/orderService';
import { Order } from '../types';

const { Option } = Select;
const { Title, Text } = Typography;
const { RangePicker } = DatePicker;

function OrderManagement() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [orderData, setOrderData] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  
  // 加载订单数据
  useEffect(() => {
    const loadOrders = async () => {
      try {
        setLoading(true);
        const response = await orderService.getOrders();
        setOrderData(response.data || []);
      } catch (error: any) {
        console.error('加载订单数据失败:', error);
        message.error('加载订单数据失败');
      } finally {
        setLoading(false);
      }
    };
    
    loadOrders();
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
        let status: 'success' | 'warning' | 'default' = 'default';
        if (text === '已完成') status = 'success';
        if (text === '待支付') status = 'warning';
        return <Badge status={status} text={text} />;
      }
    },
    { title: '日期', dataIndex: 'date', key: 'date' },
    { 
      title: '操作', 
      key: 'action', 
      render: (_: any, record: Order) => (
        <Space size="middle">
          <Button type="primary" icon={<EyeOutlined />} size="small" onClick={() => handleView(record)}>
            查看
          </Button>
          <Button icon={<EditOutlined />} size="small" onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Button danger icon={<DeleteOutlined />} size="small" onClick={() => handleDelete(record.orderId)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];

  const handleView = async (order: Order) => {
    try {
      // 加载订单详情
      const response = await orderService.getOrder(order.orderId);
      setSelectedOrder(response.data || order);
      setIsModalOpen(true);
    } catch (error: any) {
      console.error('加载订单详情失败:', error);
      message.error('加载订单详情失败');
      // 即使失败也打开模态框，使用基本信息
      setSelectedOrder(order);
      setIsModalOpen(true);
    }
  };

  const handleEdit = (order: Order) => {
    message.success(`编辑订单: ${order.orderId}`);
    // 实际项目中这里应该打开编辑模态框
  };

  const handleDelete = async (orderId: string) => {
    try {
      await orderService.deleteOrder(orderId);
      message.success(`删除订单: ${orderId} 成功`);
      // 重新加载订单数据
      const response = await orderService.getOrders();
      setOrderData(response.data || []);
    } catch (error: any) {
      console.error('删除订单失败:', error);
      message.error('删除订单失败');
    }
  };

  return (
    <div>
      <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
        <Title level={4}>订单管理</Title>
      </Space>
      
      <Card>
        <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
          <Space>
            <Input placeholder="搜索订单" prefix={<SearchOutlined />} style={{ width: 200 }} />
            <Select placeholder="状态" style={{ width: 120 }}>
              <Option value="">全部</Option>
              <Option value="待支付">待支付</Option>
              <Option value="处理中">处理中</Option>
              <Option value="已完成">已完成</Option>
              <Option value="已取消">已取消</Option>
            </Select>
            <RangePicker style={{ width: 300 }} />
          </Space>
          <Button>导出</Button>
        </Space>
        
        <Table dataSource={orderData} columns={columns} loading={loading} />
      </Card>
      
      <Modal
        title="订单详情"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
        width={600}
      >
        {selectedOrder && (
          <div>
            <Space orientation="vertical" style={{ width: '100%' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Text strong>订单编号:</Text>
                <Text>{selectedOrder.orderId}</Text>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Text strong>客户:</Text>
                <Text>{selectedOrder.customer}</Text>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Text strong>金额:</Text>
                <Text>¥{selectedOrder.amount}</Text>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Text strong>状态:</Text>
                <Text>
                  {(() => {
                    let status: 'success' | 'warning' | 'error' | 'default' = 'default';
                    if (selectedOrder.status === '已完成') status = 'success';
                    if (selectedOrder.status === '待支付') status = 'warning';
                    if (selectedOrder.status === '已取消') status = 'error';
                    return <Badge status={status} text={selectedOrder.status} />;
                  })()}
                </Text>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Text strong>日期:</Text>
                <Text>{selectedOrder.date}</Text>
              </div>
              <div style={{ marginTop: 16 }}>
                <Text strong>商品详情:</Text>
                <Table 
                  dataSource={[
                    { key: '1', product: '智能手表', quantity: 1, price: 12800 },
                  ]}
                  columns={[
                    { title: '商品', dataIndex: 'product' },
                    { title: '数量', dataIndex: 'quantity' },
                    { title: '价格', dataIndex: 'price', render: (text) => `¥${text}` },
                  ]}
                  pagination={false}
                  style={{ marginTop: 8 }}
                />
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 16 }}>
                <Button onClick={() => setIsModalOpen(false)}>关闭</Button>
              </div>
            </Space>
          </div>
        )}
      </Modal>
    </div>
  );
}

export default OrderManagement;