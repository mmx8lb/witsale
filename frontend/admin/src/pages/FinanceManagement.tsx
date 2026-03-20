import { Card, Table, Button, Space, Input, Select, Typography, message, Modal, Form, Badge, DatePicker, InputNumber } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  SearchOutlined
} from '@ant-design/icons';
import { useState } from 'react';

const { Option } = Select;
const { Title, Text } = Typography;
const { RangePicker } = DatePicker;

function FinanceManagement() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingFinance, setEditingFinance] = useState<any>(null);
  
  // 模拟财务数据
  const financeData = [
    { key: '1', id: 'F001', type: '收入', amount: 12800, date: '2026-03-20', status: '已完成', description: '销售智能手表' },
    { key: '2', id: 'F002', type: '支出', amount: 8500, date: '2026-03-19', status: '已完成', description: '采购原材料' },
    { key: '3', id: 'F003', type: '收入', amount: 15600, date: '2026-03-18', status: '已完成', description: '销售笔记本电脑' },
    { key: '4', id: 'F004', type: '支出', amount: 9200, date: '2026-03-17', status: '处理中', description: '支付运费' },
    { key: '5', id: 'F005', type: '收入', amount: 6800, date: '2026-03-16', status: '已完成', description: '销售无线耳机' },
  ];

  const columns = [
    { title: '财务ID', dataIndex: 'id', key: 'id' },
    { 
      title: '类型', 
      dataIndex: 'type', 
      key: 'type',
      render: (text: string) => (
        <Badge 
          status={text === '收入' ? 'success' : 'error'} 
          text={text} 
        />
      )
    },
    { title: '金额', dataIndex: 'amount', key: 'amount', render: (text: number, record: any) => (
      <Text style={{ color: record.type === '收入' ? 'green' : 'red' }}>
        {record.type === '收入' ? '+' : '-'}{text}
      </Text>
    )},
    { title: '日期', dataIndex: 'date', key: 'date' },
    { 
      title: '状态', 
      dataIndex: 'status', 
      key: 'status',
      render: (text: string) => (
        <Badge 
          status={text === '已完成' ? 'success' : 'processing'} 
          text={text} 
        />
      )
    },
    { title: '描述', dataIndex: 'description', key: 'description' },
    { 
      title: '操作', 
      key: 'action', 
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button type="primary" icon={<EditOutlined />} size="small" onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Button danger icon={<DeleteOutlined />} size="small" onClick={() => handleDelete(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];

  const handleAdd = () => {
    setEditingFinance(null);
    setIsModalOpen(true);
  };

  const handleEdit = (finance: any) => {
    setEditingFinance(finance);
    setIsModalOpen(true);
  };

  const handleDelete = (id: string) => {
    message.success(`删除财务记录 ID: ${id}`);
    // 实际项目中这里应该调用删除API
  };

  const handleSubmit = (values: any) => {
    if (editingFinance) {
      message.success(`更新财务记录: ${values.description}`);
    } else {
      message.success(`添加财务记录: ${values.description}`);
    }
    setIsModalOpen(false);
    // 实际项目中这里应该调用添加或更新API
  };

  return (
    <div>
      <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
        <Title level={4}>财务管理</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          添加财务记录
        </Button>
      </Space>
      
      <Card>
        <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
          <Space>
            <Input placeholder="搜索财务记录" prefix={<SearchOutlined />} style={{ width: 200 }} />
            <Select placeholder="类型" style={{ width: 120 }}>
              <Option value="">全部</Option>
              <Option value="收入">收入</Option>
              <Option value="支出">支出</Option>
            </Select>
            <Select placeholder="状态" style={{ width: 120 }}>
              <Option value="">全部</Option>
              <Option value="已完成">已完成</Option>
              <Option value="处理中">处理中</Option>
            </Select>
            <RangePicker style={{ width: 300 }} />
          </Space>
          <Button>导出</Button>
        </Space>
        
        <Table dataSource={financeData} columns={columns} />
      </Card>
      
      <Modal
        title={editingFinance ? '编辑财务记录' : '添加财务记录'}
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form
          initialValues={editingFinance || undefined}
          onFinish={handleSubmit}
          layout="vertical"
        >
          <Form.Item name="type" label="类型" rules={[{ required: true, message: '请选择类型!' }]}>
            <Select>
              <Option value="收入">收入</Option>
              <Option value="支出">支出</Option>
            </Select>
          </Form.Item>
          <Form.Item name="amount" label="金额" rules={[{ required: true, message: '请输入金额!' }]}>
            <InputNumber style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="date" label="日期" rules={[{ required: true, message: '请选择日期!' }]}>
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="status" label="状态" rules={[{ required: true, message: '请选择状态!' }]}>
            <Select>
              <Option value="已完成">已完成</Option>
              <Option value="处理中">处理中</Option>
            </Select>
          </Form.Item>
          <Form.Item name="description" label="描述" rules={[{ required: true, message: '请输入描述!' }]}>
            <Input.TextArea />
          </Form.Item>
          <Form.Item>
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsModalOpen(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                {editingFinance ? '更新' : '添加'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

export default FinanceManagement;