import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Table, Button, Modal, Form, Input, InputNumber, Select, message, Typography, Space, Card, Row, Col, ConfigProvider } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, ProductOutlined, SearchOutlined } from '@ant-design/icons'
import { getProducts, createProduct, updateProduct, deleteProduct } from '@/store/productsSlice'

const { Option } = Select
const { Title, Text, Paragraph } = Typography

const Products = () => {
  const dispatch = useDispatch()
  const { products, isLoading } = useSelector((state: any) => state.products)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState<any>(null)
  const [form] = Form.useForm()
  const [searchText, setSearchText] = useState('')

  useEffect(() => {
    dispatch(getProducts() as any)
  }, [dispatch])

  const handleAdd = () => {
    setEditingProduct(null)
    form.resetFields()
    setIsModalOpen(true)
  }

  const handleEdit = (product: any) => {
    setEditingProduct(product)
    form.setFieldsValue(product)
    setIsModalOpen(true)
  }

  const handleDelete = async (productId: number) => {
    try {
      await (dispatch(deleteProduct(productId) as any)).unwrap()
      message.success('商品删除成功')
    } catch (err) {
      message.error('商品删除失败')
    }
  }

  const handleSubmit = async (values: any) => {
    try {
      if (editingProduct) {
        await (dispatch(updateProduct({ ...values, id: editingProduct.id }) as any)).unwrap()
        message.success('商品更新成功')
      } else {
        await (dispatch(createProduct(values) as any)).unwrap()
        message.success('商品创建成功')
      }
      setIsModalOpen(false)
    } catch (err) {
      message.error('操作失败')
    }
  }

  const columns = [
    { 
      title: 'ID', 
      dataIndex: 'id', 
      key: 'id',
      width: 80,
      sorter: (a: any, b: any) => a.id - b.id,
      render: (id: number) => (
        <Text style={{ fontWeight: 500, color: '#333' }}>{id}</Text>
      )
    },
    { 
      title: '商品名称', 
      dataIndex: 'name', 
      key: 'name',
      ellipsis: true,
      sorter: (a: any, b: any) => a.name.localeCompare(b.name),
      render: (name: string) => (
        <Text style={{ fontWeight: 500, color: '#333' }}>{name}</Text>
      )
    },
    { 
      title: '商品编码', 
      dataIndex: 'code', 
      key: 'code',
      ellipsis: true,
      render: (code: string) => (
        <Text style={{ color: '#666' }}>{code}</Text>
      )
    },
    {
      title: '价格', 
      dataIndex: 'price', 
      key: 'price', 
      sorter: (a: any, b: any) => a.price - b.price,
      render: (price: number) => (
        <Text style={{ color: '#1890ff', fontWeight: 500, fontSize: '14px' }}>¥{price}</Text>
      ),
      align: 'right' as const
    },
    {
      title: '库存', 
      dataIndex: 'stock', 
      key: 'stock',
      align: 'right' as const,
      sorter: (a: any, b: any) => a.stock - b.stock,
      render: (stock: number) => (
        <Text style={{ 
          color: stock > 0 ? '#52c41a' : '#ff4d4f',
          fontWeight: 500
        }}>
          {stock}
        </Text>
      )
    },
    { 
      title: '状态', 
      dataIndex: 'status', 
      key: 'status',
      filters: [
        { text: '激活', value: 'active' },
        { text: '停用', value: 'inactive' },
      ],
      onFilter: (value: any, record: any) => record.status === value,
      render: (status: string) => (
        <Text style={{ 
          color: status === 'active' ? '#52c41a' : '#faad14'
        }}>
          {status === 'active' ? '激活' : '停用'}
        </Text>
      )
    },
    {
      title: '操作', 
      key: 'action',
      align: 'center' as const,
      render: (_: any, record: any) => (
        <Space size={8}>
          <Button 
            type="primary" 
            icon={<EditOutlined />} 
            onClick={() => handleEdit(record)}
            size="small"
            style={{ borderColor: '#1890ff', color: '#1890ff' }}
            shape="circle"
          />
          <Button 
            danger 
            icon={<DeleteOutlined />} 
            onClick={() => handleDelete(record.id)}
            size="small"
            shape="circle"
          />
        </Space>
      )
    },
  ]

  return (
    <>
      {/* 页面头部 */}
      <div style={{ marginBottom: '32px' }}>
        <Title level={2} style={{ 
          marginBottom: '8px',
          color: '#333',
          fontWeight: 600
        }}>
          <Space size={8}>
            <ProductOutlined style={{ color: '#1890ff' }} />
            商品管理
          </Space>
        </Title>
        <Paragraph type="secondary" style={{ marginBottom: 0 }}>
          管理商品信息，包括添加、编辑和删除操作
        </Paragraph>
      </div>
        
        {/* 操作区域 */}
        <Card 
          style={{ 
            marginBottom: '24px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
            borderRadius: '12px',
            border: 'none'
          }}
          bodyStyle={{
            padding: '24px'
          }}
        >
          <Row align="middle" gutter={16}>
            <Col flex="auto">
              <Text style={{ fontSize: '14px', color: '#666' }}>
                共有 <Text style={{ color: '#1890ff', fontWeight: 500 }}>{products.length}</Text> 个商品
              </Text>
            </Col>
            <Col xs={24} sm={12} md={8} lg={6}>
              <Input
                placeholder="搜索商品名称或编码"
                prefix={<SearchOutlined />}
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                style={{ width: '100%' }}
              />
            </Col>
            <Col>
              <Button 
                type="primary" 
                icon={<PlusOutlined />} 
                onClick={handleAdd}
                size="large"
                style={{
                  borderRadius: '6px',
                  padding: '0 24px'
                }}
              >
                添加商品
              </Button>
            </Col>
          </Row>
        </Card>
        
        {/* 商品表格 */}
        <Card 
          style={{ 
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
            borderRadius: '12px',
            border: 'none'
          }}
          bodyStyle={{
            padding: '24px'
          }}
        >
          <Table 
            columns={columns} 
            dataSource={products} 
            rowKey="id" 
            loading={isLoading}
            pagination={{ 
              pageSize: 10,
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total) => `共 ${total} 条记录`,
              style: {
                marginTop: '24px'
              }
            }}
            scroll={{ x: 800 }}
            rowClassName="hover:bg-gray-50"
            onRow={() => ({
              onMouseEnter: (e) => {
                e.currentTarget.style.backgroundColor = '#f5f5f5'
              },
              onMouseLeave: (e) => {
                e.currentTarget.style.backgroundColor = '#fff'
              }
            })}
            style={{
              width: '100%'
            }}
          />
        </Card>
        
        {/* 模态框 */}
        <Modal
          title={
            <Space size={8}>
              {editingProduct ? <EditOutlined style={{ color: '#1890ff' }} /> : <PlusOutlined style={{ color: '#1890ff' }} />}
              <Text style={{ 
                fontSize: '16px', 
                fontWeight: 600,
                color: '#333'
              }}>
                {editingProduct ? '编辑商品' : '添加商品'}
              </Text>
            </Space>
          }
          open={isModalOpen}
          onCancel={() => setIsModalOpen(false)}
          footer={null}
          width={600}
          style={{ borderRadius: '12px' }}
          bodyStyle={{
            padding: '24px'
          }}
        >
          <Form 
            form={form} 
            layout="vertical" 
            onFinish={handleSubmit}
            style={{ maxWidth: '100%' }}
          >
            <Row gutter={24}>
              <Col span={12}>
                <Form.Item 
                  name="name" 
                  label="商品名称" 
                  rules={[{ required: true, message: '请输入商品名称' }]}
                  labelCol={{ span: 24 }}
                  wrapperCol={{ span: 24 }}
                >
                  <Input 
                    placeholder="请输入商品名称" 
                    style={{ borderRadius: '6px' }}
                  />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item 
                  name="code" 
                  label="商品编码" 
                  rules={[{ required: true, message: '请输入商品编码' }]}
                  labelCol={{ span: 24 }}
                  wrapperCol={{ span: 24 }}
                >
                  <Input 
                    placeholder="请输入商品编码" 
                    style={{ borderRadius: '6px' }}
                  />
                </Form.Item>
              </Col>
            </Row>
            <Row gutter={24}>
              <Col span={12}>
                <Form.Item 
                  name="price" 
                  label="价格" 
                  rules={[{ required: true, type: 'number', min: 0, message: '请输入有效价格' }]}
                  labelCol={{ span: 24 }}
                  wrapperCol={{ span: 24 }}
                >
                  <InputNumber 
                    style={{ width: '100%', borderRadius: '6px' }} 
                    placeholder="请输入价格"
                    formatter={(value) => `¥ ${value}`}
                    parser={(value) => value ? value.replace(/¥\s?|(,*)/g, '') : ''}
                  />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item 
                  name="stock" 
                  label="库存" 
                  rules={[{ required: true, type: 'number', min: 0, message: '请输入有效库存' }]}
                  labelCol={{ span: 24 }}
                  wrapperCol={{ span: 24 }}
                >
                  <InputNumber 
                    style={{ width: '100%', borderRadius: '6px' }} 
                    placeholder="请输入库存"
                  />
                </Form.Item>
              </Col>
            </Row>
            <Form.Item 
              name="status" 
              label="状态" 
              rules={[{ required: true, message: '请选择状态' }]}
              labelCol={{ span: 24 }}
              wrapperCol={{ span: 24 }}
            >
              <Select 
                placeholder="请选择状态" 
                style={{ width: '100%', borderRadius: '6px' }}
              >
                <Option value="active">激活</Option>
                <Option value="inactive">停用</Option>
              </Select>
            </Form.Item>
            <Form.Item style={{ textAlign: 'right', marginTop: '32px' }}>
              <Space size={12}>
                <Button 
                  onClick={() => setIsModalOpen(false)}
                  style={{ borderRadius: '6px', padding: '0 24px' }}
                >
                  取消
                </Button>
                <Button 
                  type="primary" 
                  htmlType="submit"
                  style={{ borderRadius: '6px', padding: '0 32px' }}
                >
                  保存
                </Button>
              </Space>
            </Form.Item>
          </Form>
        </Modal>
    </>
  )
}

export { Products }