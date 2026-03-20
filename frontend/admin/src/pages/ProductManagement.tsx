import { Card, Table, Button, Space, Input, Select, Typography, message, Modal, Form, Upload, TreeSelect, Descriptions, Badge, Divider } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  SearchOutlined,
  UploadOutlined,
  FolderOutlined,
  BarcodeOutlined,
  DollarOutlined
} from '@ant-design/icons';
import { useState, useEffect } from 'react';
import productService from '../services/productService';
import { Product, Category, Sku } from '../types';

const { Option } = Select;
const { Title } = Typography;
const { Dragger } = Upload;

function ProductManagement() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);
  const [isSkuModalOpen, setIsSkuModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [productData, setProductData] = useState<Product[]>([]);
  const [categoryData, setCategoryData] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  
  // 加载商品数据
  useEffect(() => {
    const loadProducts = async () => {
      try {
        setLoading(true);
        const response = await productService.getProducts();
        setProductData(response.data || []);
      } catch (error: any) {
        console.error('加载商品数据失败:', error);
        message.error('加载商品数据失败');
      } finally {
        setLoading(false);
      }
    };
    
    loadProducts();
  }, []);
  
  // 加载分类数据
  useEffect(() => {
    const loadCategories = async () => {
      try {
        const response = await productService.getCategories();
        setCategoryData(response.data || []);
      } catch (error: any) {
        console.error('加载分类数据失败:', error);
      }
    };
    
    loadCategories();
  }, []);

  const columns = [
    { title: '商品ID', dataIndex: 'id', key: 'id' },
    { title: '商品名称', dataIndex: 'name', key: 'name' },
    { title: '分类', dataIndex: 'category', key: 'category' },
    { 
      title: '状态', 
      dataIndex: 'status', 
      key: 'status',
      render: (text: string) => (
        <Badge 
          status={text === 'active' ? 'success' : 'default'} 
          text={text === 'active' ? '上架' : '下架'} 
        />
      )
    },
    { title: 'SKU数量', dataIndex: 'skus', key: 'skuCount', render: (skus: Sku[]) => skus?.length || 0 },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
    { title: '更新时间', dataIndex: 'updated_at', key: 'updated_at' },
    { 
      title: '操作', 
      key: 'action', 
      render: (_: any, record: Product) => (
        <Space size="middle">
          <Button type="primary" icon={<EditOutlined />} size="small" onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Button icon={<BarcodeOutlined />} size="small" onClick={() => handleSkuManagement(record)}>
            SKU管理
          </Button>
          <Button danger icon={<DeleteOutlined />} size="small" onClick={() => handleDelete(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];

  const handleAdd = () => {
    setEditingProduct(null);
    setIsModalOpen(true);
  };

  const handleEdit = (product: Product) => {
    setEditingProduct(product);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    try {
      await productService.deleteProduct(id);
      message.success(`删除商品 ID: ${id} 成功`);
      // 重新加载商品数据
      const response = await productService.getProducts();
      setProductData(response.data || []);
    } catch (error: any) {
      console.error('删除商品失败:', error);
      message.error('删除商品失败');
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      if (editingProduct) {
        await productService.updateProduct(editingProduct.id, values);
        message.success(`更新商品: ${values.name} 成功`);
      } else {
        await productService.createProduct(values);
        message.success(`添加商品: ${values.name} 成功`);
      }
      setIsModalOpen(false);
      // 重新加载商品数据
      const response = await productService.getProducts();
      setProductData(response.data || []);
    } catch (error: any) {
      console.error('保存商品失败:', error);
      message.error('保存商品失败');
    }
  };
  
  const handleCategoryManagement = () => {
    setIsCategoryModalOpen(true);
  };
  
  const handleSkuManagement = async (product: Product) => {
    try {
      // 加载商品的SKU数据
      const skuResponse = await productService.getSkus(product.id);
      const productWithSkus = {
        ...product,
        skus: skuResponse.data || []
      };
      setSelectedProduct(productWithSkus);
      setIsSkuModalOpen(true);
    } catch (error: any) {
      console.error('加载SKU数据失败:', error);
      message.error('加载SKU数据失败');
      // 即使失败也打开模态框，使用商品基本信息
      setSelectedProduct(product);
      setIsSkuModalOpen(true);
    }
  };

  return (
    <div>
      <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
        <Title level={4}>商品管理</Title>
        <Space>
          <Button icon={<FolderOutlined />} onClick={handleCategoryManagement}>
            分类管理
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加商品
          </Button>
        </Space>
      </Space>
      
      <Card>
        <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
          <Space>
            <Input placeholder="搜索商品" prefix={<SearchOutlined />} style={{ width: 200 }} />
            <Select placeholder="分类" style={{ width: 120 }}>
              <Option value="">全部</Option>
              <Option value="电子产品">电子产品</Option>
              <Option value="服装">服装</Option>
              <Option value="食品">食品</Option>
            </Select>
            <Select placeholder="状态" style={{ width: 120 }}>
              <Option value="">全部</Option>
              <Option value="上架">上架</Option>
              <Option value="下架">下架</Option>
            </Select>
          </Space>
          <Button>导出</Button>
        </Space>
        
        <Table dataSource={productData} columns={columns} loading={loading} />
      </Card>
      
      <Modal
        title={editingProduct ? '编辑商品' : '添加商品'}
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form
          initialValues={editingProduct || undefined}
          onFinish={handleSubmit}
          layout="vertical"
        >
          <Form.Item name="name" label="商品名称" rules={[{ required: true, message: '请输入商品名称!' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="categoryId" label="分类" rules={[{ required: true, message: '请选择分类!' }]}>
            <TreeSelect
              treeData={categoryData}
              placeholder="选择分类"
              style={{ width: '100%' }}
            />
          </Form.Item>
          <Form.Item name="description" label="商品描述">
            <Input.TextArea rows={4} />
          </Form.Item>
          <Form.Item name="specs" label="商品规格">
            <Input.TextArea rows={3} placeholder='JSON格式，例如: {"size": "M", "color": "red"}' />
          </Form.Item>
          <Form.Item name="attributes" label="商品属性">
            <Input.TextArea rows={3} placeholder='JSON格式，例如: {"material": "cotton", "weight": "200g"}' />
          </Form.Item>
          <Form.Item name="status" label="状态" rules={[{ required: true, message: '请选择状态!' }]}>
            <Select>
              <Option value="active">上架</Option>
              <Option value="inactive">下架</Option>
            </Select>
          </Form.Item>
          <Form.Item name="image" label="商品图片">
            <Dragger name="file" action="https://run.mocky.io/v3/435e224c-44fb-4773-9faf-380c5e6a2188" listType="picture">
              <p className="ant-upload-drag-icon">
                <UploadOutlined />
              </p>
              <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
              <p className="ant-upload-hint">支持 JPG、PNG 格式，最大 5MB</p>
            </Dragger>
          </Form.Item>
          <Form.Item>
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsModalOpen(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                {editingProduct ? '更新' : '添加'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
      
      {/* 分类管理模态框 */}
      <Modal
        title="分类管理"
        open={isCategoryModalOpen}
        onCancel={() => setIsCategoryModalOpen(false)}
        footer={null}
        width={600}
      >
        <Space direction="vertical" style={{ width: '100%' }}>
          <Space style={{ width: '100%', justifyContent: 'space-between' }}>
            <Title level={5}>分类列表</Title>
            <Button type="primary" icon={<PlusOutlined />}>
              添加分类
            </Button>
          </Space>
          <Card>
            <Table 
              dataSource={[
                { key: '1', id: 'C001', name: '电子产品', parent: '无', level: 1, sortOrder: 1 },
                { key: '2', id: 'C001-1', name: '手机', parent: '电子产品', level: 2, sortOrder: 1 },
                { key: '3', id: 'C001-2', name: '电脑', parent: '电子产品', level: 2, sortOrder: 2 },
                { key: '4', id: 'C002', name: '服装', parent: '无', level: 1, sortOrder: 2 },
                { key: '5', id: 'C003', name: '食品', parent: '无', level: 1, sortOrder: 3 },
              ]}
              columns={[
                { title: '分类ID', dataIndex: 'id', key: 'id' },
                { title: '分类名称', dataIndex: 'name', key: 'name' },
                { title: '父分类', dataIndex: 'parent', key: 'parent' },
                { title: '层级', dataIndex: 'level', key: 'level' },
                { title: '排序', dataIndex: 'sortOrder', key: 'sortOrder' },
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
            <Button onClick={() => setIsCategoryModalOpen(false)}>关闭</Button>
          </Space>
        </Space>
      </Modal>
      
      {/* SKU管理模态框 */}
      <Modal
        title={`SKU管理 - ${selectedProduct?.name}`}
        open={isSkuModalOpen}
        onCancel={() => setIsSkuModalOpen(false)}
        footer={null}
        width={800}
      >
        {selectedProduct && (
          <Space orientation="vertical" style={{ width: '100%' }}>
            <Space style={{ width: '100%', justifyContent: 'space-between' }}>
              <Title level={5}>SKU列表</Title>
              <Button type="primary" icon={<PlusOutlined />}>
                添加SKU
              </Button>
            </Space>
            
            <Card>
              <Table 
                dataSource={selectedProduct.skus}
                columns={[
                  { title: 'SKU ID', dataIndex: 'id', key: 'id' },
                  { title: 'SKU编码', dataIndex: 'sku_code', key: 'sku_code' },
                  { title: 'SKU名称', dataIndex: 'name', key: 'name' },
                  { title: '价格', dataIndex: 'price', key: 'price', render: (text) => `¥${text}` },
                  { title: '库存', dataIndex: 'stock', key: 'stock' },
                  {
                    title: '操作',
                    key: 'action',
                    render: (_) => (
                    <Space size="middle">
                      <Button type="primary" icon={<EditOutlined />} size="small">
                        编辑
                      </Button>
                      <Button icon={<DollarOutlined />} size="small">
                        价格管理
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
            
            <Divider>SKU详情</Divider>
            
            <Card>
              <Descriptions column={2}>
                <Descriptions.Item label="商品名称">{selectedProduct.name}</Descriptions.Item>
                <Descriptions.Item label="商品ID">{selectedProduct.id}</Descriptions.Item>
                <Descriptions.Item label="分类">{selectedProduct.category}</Descriptions.Item>
                <Descriptions.Item label="状态">
                  <Badge 
                    status={selectedProduct.status === 'active' ? 'success' : 'default'} 
                    text={selectedProduct.status === 'active' ? '上架' : '下架'} 
                  />
                </Descriptions.Item>
                <Descriptions.Item label="创建时间">{selectedProduct.created_at}</Descriptions.Item>
                <Descriptions.Item label="更新时间">{selectedProduct.updated_at}</Descriptions.Item>
                <Descriptions.Item label="描述" span={2}>{selectedProduct.description}</Descriptions.Item>
              </Descriptions>
            </Card>
            
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsSkuModalOpen(false)}>关闭</Button>
            </Space>
          </Space>
        )}
      </Modal>
    </div>
  );
}

export default ProductManagement;