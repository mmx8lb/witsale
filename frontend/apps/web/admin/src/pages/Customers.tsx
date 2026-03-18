import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Table, Button, Modal, Form, Input, Select, message } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import { getCustomers, createCustomer, updateCustomer, deleteCustomer } from '@/store/customersSlice'

const { Option } = Select

const Customers = () => {
  const dispatch = useDispatch()
  const { customers, isLoading, error } = useSelector((state: any) => state.customers)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingCustomer, setEditingCustomer] = useState<any>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    dispatch(getCustomers())
  }, [dispatch])

  const handleAdd = () => {
    setEditingCustomer(null)
    form.resetFields()
    setIsModalOpen(true)
  }

  const handleEdit = (customer: any) => {
    setEditingCustomer(customer)
    form.setFieldsValue(customer)
    setIsModalOpen(true)
  }

  const handleDelete = async (customerId: number) => {
    try {
      await dispatch(deleteCustomer(customerId)).unwrap()
      message.success('客户删除成功')
    } catch (err) {
      message.error('客户删除失败')
    }
  }

  const handleSubmit = async (values: any) => {
    try {
      if (editingCustomer) {
        await dispatch(updateCustomer({ ...values, id: editingCustomer.id })).unwrap()
        message.success('客户更新成功')
      } else {
        await dispatch(createCustomer(values)).unwrap()
        message.success('客户创建成功')
      }
      setIsModalOpen(false)
    } catch (err) {
      message.error('操作失败')
    }
  }

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '客户名称', dataIndex: 'name', key: 'name' },
    { title: '客户编码', dataIndex: 'code', key: 'code' },
    { title: '客户类型', dataIndex: 'type', key: 'type' },
    { title: '客户等级', dataIndex: 'level', key: 'level' },
    { title: '联系人', dataIndex: 'contact', key: 'contact' },
    { title: '联系电话', dataIndex: 'phone', key: 'phone' },
    { title: '状态', dataIndex: 'status', key: 'status' },
    { 
      title: '操作', 
      key: 'action',
      render: (_: any, record: any) => (
        <div>
          <Button icon={<EditOutlined />} onClick={() => handleEdit(record)} style={{ marginRight: 8 }} />
          <Button danger icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)} />
        </div>
      )
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2>客户管理</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>添加客户</Button>
      </div>
      <Table 
        columns={columns} 
        dataSource={customers} 
        rowKey="id" 
        loading={isLoading}
        pagination={{ pageSize: 10 }}
      />
      
      <Modal
        title={editingCustomer ? '编辑客户' : '添加客户'}
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="name" label="客户名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="code" label="客户编码" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="type" label="客户类型" rules={[{ required: true }]}>
            <Select>
              <Option value="enterprise">企业客户</Option>
              <Option value="channel">渠道客户</Option>
              <Option value="terminal">终端客户</Option>
              <Option value="individual">个人客户</Option>
            </Select>
          </Form.Item>
          <Form.Item name="level" label="客户等级" rules={[{ required: true }]}>
            <Select>
              <Option value="platinum">白金</Option>
              <Option value="gold">黄金</Option>
              <Option value="silver">白银</Option>
              <Option value="bronze">青铜</Option>
            </Select>
          </Form.Item>
          <Form.Item name="contact" label="联系人" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="phone" label="联系电话" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="status" label="状态" rules={[{ required: true }]}>
            <Select>
              <Option value="active">激活</Option>
              <Option value="inactive">停用</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" style={{ marginRight: 8 }}>
              保存
            </Button>
            <Button onClick={() => setIsModalOpen(false)}>取消</Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export { Customers }