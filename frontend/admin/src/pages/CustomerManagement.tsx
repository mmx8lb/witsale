import { Card, Table, Button, Space, Input, Select, Typography, message, Modal, Form, Badge, Checkbox, Tag } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  SearchOutlined,
  TagsOutlined
} from '@ant-design/icons';
import { useState, useEffect } from 'react';
import customerService from '../services/customerService';
import { Customer } from '../types';

const { Option } = Select;
const { Title } = Typography;

function CustomerManagement() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState<Customer | null>(null);
  const [isTagModalOpen, setIsTagModalOpen] = useState(false);
  const [tagData, setTagData] = useState<any[]>([]);
  const [customerData, setCustomerData] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  
  // 加载标签数据
  useEffect(() => {
    const loadTags = async () => {
      try {
        const response = await customerService.getTags();
        setTagData(response.data || []);
      } catch (error: any) {
        console.error('加载标签数据失败:', error);
      }
    };
    
    loadTags();
  }, []);
  
  // 加载客户数据
  useEffect(() => {
    const loadCustomers = async () => {
      try {
        setLoading(true);
        const response = await customerService.getCustomers();
        setCustomerData(response.data || []);
      } catch (error: any) {
        console.error('加载客户数据失败:', error);
        message.error('加载客户数据失败');
      } finally {
        setLoading(false);
      }
    };
    
    loadCustomers();
  }, []);


  const columns = [
    { title: '客户ID', dataIndex: 'id', key: 'id' },
    { title: '客户名称', dataIndex: 'name', key: 'name' },
    { title: '电话', dataIndex: 'phone', key: 'phone' },
    { title: '邮箱', dataIndex: 'email', key: 'email' },
    { 
      title: '客户等级', 
      dataIndex: 'level', 
      key: 'level',
      render: (text: string) => (
        <Badge 
          status={text === 'VIP' ? 'success' : 'default'} 
          text={text} 
        />
      )
    },
    { 
      title: '状态', 
      dataIndex: 'status', 
      key: 'status',
      render: (text: string) => (
        <Badge 
          status={text === '活跃' ? 'success' : 'default'} 
          text={text} 
        />
      )
    },
    { 
      title: '标签', 
      dataIndex: 'tags', 
      key: 'tags',
      render: (tags: string[]) => (
        <Space>
          {tags.map(tagId => {
            const tag = tagData.find(t => t.id === tagId);
            return tag ? <Tag color={tag.color} key={tag.id}>{tag.name}</Tag> : null;
          })}
        </Space>
      )
    },
    { 
      title: '操作', 
      key: 'action', 
      render: (_: any, record: Customer) => (
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
    setEditingCustomer(null);
    setIsModalOpen(true);
  };

  const handleEdit = (customer: Customer) => {
    setEditingCustomer(customer);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    try {
      await customerService.deleteCustomer(id);
      message.success(`删除客户 ID: ${id} 成功`);
      // 重新加载客户数据
      const response = await customerService.getCustomers();
      setCustomerData(response.data || []);
    } catch (error) {
      console.error('删除客户失败:', error);
      message.error('删除客户失败');
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      if (editingCustomer) {
        await customerService.updateCustomer(editingCustomer.id, values);
        message.success(`更新客户: ${values.name} 成功`);
      } else {
        await customerService.createCustomer(values);
        message.success(`添加客户: ${values.name} 成功`);
      }
      setIsModalOpen(false);
      // 重新加载客户数据
      const response = await customerService.getCustomers();
      setCustomerData(response.data || []);
    } catch (error) {
      console.error('保存客户失败:', error);
      message.error('保存客户失败');
    }
  };
  
  const handleTagManagement = () => {
    setIsTagModalOpen(true);
  };

  return (
    <div>
      <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
        <Title level={4}>客户管理</Title>
        <Space>
          <Button icon={<TagsOutlined />} onClick={handleTagManagement}>
            标签管理
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加客户
          </Button>
        </Space>
      </Space>
      
      <Card>
        <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
          <Space>
            <Input placeholder="搜索客户" prefix={<SearchOutlined />} style={{ width: 200 }} />
            <Select placeholder="客户等级" style={{ width: 120 }}>
              <Option value="">全部</Option>
              <Option value="VIP">VIP</Option>
              <Option value="普通">普通</Option>
            </Select>
            <Select placeholder="状态" style={{ width: 120 }}>
              <Option value="">全部</Option>
              <Option value="活跃">活跃</Option>
              <Option value="inactive">非活跃</Option>
            </Select>
          </Space>
          <Button>导出</Button>
        </Space>
        
        <Table dataSource={customerData} columns={columns} loading={loading} />
      </Card>
      
      <Modal
        title={editingCustomer ? '编辑客户' : '添加客户'}
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form
          initialValues={editingCustomer || undefined}
          onFinish={handleSubmit}
          layout="vertical"
        >
          <Form.Item name="name" label="客户名称" rules={[{ required: true, message: '请输入客户名称!' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="phone" label="电话" rules={[{ required: true, message: '请输入电话!' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="email" label="邮箱" rules={[{ required: true, message: '请输入邮箱!' }]}>
            <Input type="email" />
          </Form.Item>
          <Form.Item name="level" label="客户等级" rules={[{ required: true, message: '请选择客户等级!' }]}>
            <Select>
              <Option value="VIP">VIP</Option>
              <Option value="普通">普通</Option>
            </Select>
          </Form.Item>
          <Form.Item name="status" label="状态" rules={[{ required: true, message: '请选择状态!' }]}>
            <Select>
              <Option value="活跃">活跃</Option>
              <Option value="inactive">非活跃</Option>
            </Select>
          </Form.Item>
          <Form.Item name="tags" label="标签">
            <Space orientation="vertical" style={{ width: '100%' }}>
              <Checkbox.Group>
                <Space wrap>
                  {tagData.map(tag => (
                    <Checkbox key={tag.id} value={tag.id}>
                      <Tag color={tag.color}>{tag.name}</Tag>
                    </Checkbox>
                  ))}
                </Space>
              </Checkbox.Group>
            </Space>
          </Form.Item>
          <Form.Item>
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsModalOpen(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                {editingCustomer ? '更新' : '添加'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
      
      {/* 标签管理模态框 */}
      <Modal
        title="标签管理"
        open={isTagModalOpen}
        onCancel={() => setIsTagModalOpen(false)}
        footer={null}
        width={600}
      >
        <Space orientation="vertical" style={{ width: '100%' }}>
          <Space style={{ width: '100%', justifyContent: 'space-between' }}>
            <Title level={5}>标签列表</Title>
            <Button type="primary" icon={<PlusOutlined />}>
              添加标签
            </Button>
          </Space>
          <Card>
            <Table 
              dataSource={tagData.map(tag => ({
                key: tag.id,
                id: tag.id,
                name: tag.name,
                color: tag.color
              }))}
              columns={[
                { title: '标签ID', dataIndex: 'id', key: 'id' },
                { title: '标签名称', dataIndex: 'name', key: 'name' },
                { 
                  title: '颜色', 
                  dataIndex: 'color', 
                  key: 'color',
                  render: (color) => (
                    <Tag color={color}>{color}</Tag>
                  )
                },
                {
                  title: '操作',
                  key: 'action',
                  render: (_) => (
                    <Space size="middle">
                      <Button type="primary" icon={<EditOutlined />} size="small">
                        编辑
                      </Button>
                      <Button danger icon={<DeleteOutlined />} size="small">
                        删除
                      </Button>
                    </Space>
                  ),
                },
              ]}
            />
          </Card>
          <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
            <Button onClick={() => setIsTagModalOpen(false)}>关闭</Button>
          </Space>
        </Space>
      </Modal>
    </div>
  );
}

export default CustomerManagement;