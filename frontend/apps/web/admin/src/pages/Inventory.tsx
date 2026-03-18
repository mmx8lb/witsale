import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Table, Button, Modal, Form, InputNumber, Select, message } from 'antd'
import { PlusOutlined, EditOutlined } from '@ant-design/icons'
import { getInventory, updateInventory } from '@/store/inventorySlice'

const { Option } = Select

const Inventory = () => {
  const dispatch = useDispatch()
  const { inventory, isLoading, error } = useSelector((state: any) => state.inventory)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingItem, setEditingItem] = useState<any>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    dispatch(getInventory())
  }, [dispatch])

  const handleEdit = (item: any) => {
    setEditingItem(item)
    form.setFieldsValue(item)
    setIsModalOpen(true)
  }

  const handleSubmit = async (values: any) => {
    try {
      await dispatch(updateInventory({ ...values, id: editingItem.id })).unwrap()
      message.success('库存更新成功')
      setIsModalOpen(false)
    } catch (err) {
      message.error('库存更新失败')
    }
  }

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '商品ID', dataIndex: 'product_id', key: 'product_id' },
    { title: '商品名称', dataIndex: 'product_name', key: 'product_name' },
    { title: '仓库ID', dataIndex: 'warehouse_id', key: 'warehouse_id' },
    { title: '仓库名称', dataIndex: 'warehouse_name', key: 'warehouse_name' },
    { title: '库存数量', dataIndex: 'quantity', key: 'quantity' },
    { title: '状态', dataIndex: 'status', key: 'status' },
    { 
      title: '操作', 
      key: 'action',
      render: (_: any, record: any) => (
        <Button icon={<EditOutlined />} onClick={() => handleEdit(record)} />
      )
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2>库存管理</h2>
      </div>
      <Table 
        columns={columns} 
        dataSource={inventory} 
        rowKey="id" 
        loading={isLoading}
        pagination={{ pageSize: 10 }}
      />
      
      <Modal
        title="编辑库存"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="quantity" label="库存数量" rules={[{ required: true, type: 'number', min: 0 }]}>
            <InputNumber style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="status" label="状态" rules={[{ required: true }]}>
            <Select>
              <Option value="normal">正常</Option>
              <Option value="low">低库存</Option>
              <Option value="out_of_stock">缺货</Option>
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

export { Inventory }