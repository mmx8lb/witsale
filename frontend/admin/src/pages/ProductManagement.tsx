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
import { Link } from 'react-router-dom';
import productService from '../services/productService';
import { Product, Category, Sku } from '../types';

const { Option } = Select;
const { Title } = Typography;
const { Dragger } = Upload;

function ProductManagement() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [isSkuModalOpen, setIsSkuModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [productData, setProductData] = useState<Product[]>([]);
  const [categoryData, setCategoryData] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAddSkuModalOpen, setIsAddSkuModalOpen] = useState(false);
  const [isEditSkuModalOpen, setIsEditSkuModalOpen] = useState(false);
  const [editingSku, setEditingSku] = useState<any>(null);
  const [isPriceModalOpen, setIsPriceModalOpen] = useState(false);
  const [selectedSku, setSelectedSku] = useState<any>(null);
  const [isAddPriceModalOpen, setIsAddPriceModalOpen] = useState(false);
  const [editingPrice, setEditingPrice] = useState<any>(null);
  
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
        const categories: any[] = response.data || [];
        // 转换分类数据，确保每个节点都有有效的value和title
        const transformedCategories = categories.map(category => ({
          title: category.name || '未命名分类',
          value: category.id.toString(),
          parent_id: category.parent_id ? category.parent_id.toString() : null,
          children: []
        }));
        
        // 构建树形结构
        const buildTree = (categories: any[], parentId: string | null = null): any[] => {
          return categories
            .filter(category => category.parent_id === parentId)
            .map(category => ({
              ...category,
              children: buildTree(categories, category.value)
            }));
        };
        
        const treeData = buildTree(transformedCategories);
        setCategoryData(treeData);
      } catch (error: any) {
        console.error('加载分类数据失败:', error);
      }
    };
    
    loadCategories();
  }, []);

  const columns = [
    { title: '商品ID', dataIndex: 'id', key: 'id' },
    { title: '商品名称', dataIndex: 'name', key: 'name' },
    { title: '分类', dataIndex: 'category', key: 'category', render: (category: any) => category?.name || '' },
    { title: '品牌', dataIndex: 'brand', key: 'brand' },
    { title: '型号', dataIndex: 'model', key: 'model' },
    { 
      title: '状态', 
      dataIndex: 'is_active', 
      key: 'is_active',
      render: (is_active: boolean) => (
        <Badge 
          status={is_active ? 'success' : 'default'} 
          text={is_active ? '上架' : '下架'} 
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
    // 转换商品数据，确保表单能正确显示
    const editedProduct = {
      ...product,
      category_id: product.category_id.toString()
    } as any;
    setEditingProduct(editedProduct);
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
      // 处理表单数据，确保类型正确
      const submitData = {
        ...values,
        category_id: parseInt(values.category_id),
        is_active: values.is_active === true || values.is_active === 'true'
      };
      
      if (editingProduct) {
        await productService.updateProduct(editingProduct.id, submitData);
        message.success(`更新商品: ${submitData.name} 成功`);
      } else {
        await productService.createProduct(submitData);
        message.success(`添加商品: ${submitData.name} 成功`);
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
  
  // 分类管理已移至独立页面
  
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

  const handleAddSku = () => {
    setEditingSku(null);
    setIsAddSkuModalOpen(true);
  };

  const handleEditSku = (sku: any) => {
    setEditingSku(sku);
    setIsEditSkuModalOpen(true);
  };

  const handleDeleteSku = async (skuId: string) => {
    try {
      await productService.deleteSku(skuId);
      message.success(`删除SKU ID: ${skuId} 成功`);
      // 重新加载SKU数据
      if (selectedProduct) {
        const skuResponse = await productService.getSkus(selectedProduct.id);
        const productWithSkus = {
          ...selectedProduct,
          skus: skuResponse.data || []
        };
        setSelectedProduct(productWithSkus);
      }
    } catch (error: any) {
      console.error('删除SKU失败:', error);
      message.error('删除SKU失败');
    }
  };

  const handlePriceManagement = (sku: any) => {
    setSelectedSku(sku);
    setIsPriceModalOpen(true);
  };

  const handleAddPrice = () => {
    setEditingPrice(null);
    setIsAddPriceModalOpen(true);
  };

  const handleEditPrice = (price: any) => {
    setEditingPrice(price);
    setIsAddPriceModalOpen(true);
  };

  const handleDeletePrice = async (priceId: string) => {
    try {
      await productService.deletePrice(priceId);
      message.success(`删除价格 ID: ${priceId} 成功`);
      // 重新加载SKU数据以更新价格列表
      if (selectedProduct) {
        const skuResponse = await productService.getSkus(selectedProduct.id);
        const productWithSkus = {
          ...selectedProduct,
          skus: skuResponse.data || []
        };
        setSelectedProduct(productWithSkus);
        // 更新selectedSku以反映价格变化
        if (selectedSku) {
          const updatedSku = productWithSkus.skus.find((s: any) => s.id === selectedSku.id);
          if (updatedSku) {
            setSelectedSku(updatedSku);
          }
        }
      }
    } catch (error: any) {
      console.error('删除价格失败:', error);
      message.error('删除价格失败');
    }
  };

  const handlePriceSubmit = async (values: any) => {
    try {
      if (editingPrice) {
        await productService.updatePrice(editingPrice.id, values);
        message.success(`更新价格成功`);
      } else {
        await productService.createPrice({
          sku_id: selectedSku?.id,
          ...values
        });
        message.success(`添加价格成功`);
      }
      setIsAddPriceModalOpen(false);
      // 重新加载SKU数据以更新价格列表
      if (selectedProduct) {
        const skuResponse = await productService.getSkus(selectedProduct.id);
        const productWithSkus = {
          ...selectedProduct,
          skus: skuResponse.data || []
        };
        setSelectedProduct(productWithSkus);
        // 更新selectedSku以反映价格变化
        if (selectedSku) {
          const updatedSku = productWithSkus.skus.find((s: any) => s.id === selectedSku.id);
          if (updatedSku) {
            setSelectedSku(updatedSku);
          }
        }
      }
    } catch (error: any) {
      console.error('保存价格失败:', error);
      message.error('保存价格失败');
    }
  };

  const handleSkuSubmit = async (values: any) => {
    try {
      // 处理attributes字段，确保它是有效的JSON
      let processedValues = { ...values };
      if (values.attributes) {
        try {
          processedValues.attributes = JSON.parse(values.attributes);
        } catch (e) {
          message.error('SKU属性格式错误，请输入有效的JSON');
          return;
        }
      }
      
      if (editingSku) {
        await productService.updateSku(editingSku.id, {
          product_id: selectedProduct?.id,
          ...processedValues
        });
        message.success(`更新SKU: ${processedValues.name} 成功`);
        setIsEditSkuModalOpen(false);
      } else {
        await productService.createSku({
          product_id: selectedProduct?.id,
          ...processedValues
        });
        message.success(`添加SKU: ${processedValues.name} 成功`);
        setIsAddSkuModalOpen(false);
      }
      // 重新加载SKU数据
      if (selectedProduct) {
        const skuResponse = await productService.getSkus(selectedProduct.id);
        const productWithSkus = {
          ...selectedProduct,
          skus: skuResponse.data || []
        };
        setSelectedProduct(productWithSkus);
      }
    } catch (error: any) {
      console.error('保存SKU失败:', error);
      message.error('保存SKU失败');
    }
  };

  return (
    <div>
      <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
        <Title level={4}>商品管理</Title>
        <Space>
          <Link to="/categories">
            <Button icon={<FolderOutlined />}>
              分类管理
            </Button>
          </Link>
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
        
        <Table dataSource={productData} columns={columns} loading={loading} rowKey="id" />
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
          <Form.Item name="category_id" label="分类" rules={[{ required: true, message: '请选择分类!' }]}>
            <TreeSelect
              treeData={categoryData}
              placeholder="选择分类"
              style={{ width: '100%' }}
              treeDefaultExpandAll={true}
            />
          </Form.Item>
          <Form.Item name="brand" label="品牌">
            <Input placeholder="输入商品品牌" />
          </Form.Item>
          <Form.Item name="model" label="型号">
            <Input placeholder="输入商品型号" />
          </Form.Item>
          <Form.Item name="description" label="商品描述">
            <Input.TextArea rows={4} />
          </Form.Item>
          <Form.Item name="is_active" label="状态" rules={[{ required: true, message: '请选择状态!' }]}>
            <Select>
              <Option value={true}>上架</Option>
              <Option value={false}>下架</Option>
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
              <Button type="primary" icon={<PlusOutlined />} onClick={handleAddSku}>
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
                  { title: '价格', key: 'price', render: (_, record) => {
                    if (record.prices && record.prices.length > 0) {
                      return `¥${record.prices[0].price}`;
                    }
                    return '暂无价格';
                  } },
                  { title: '库存', dataIndex: 'stock', key: 'stock' },
                  {
                    title: '操作',
                    key: 'action',
                    render: (_: any, record: any) => (
                    <Space size="middle">
                      <Button type="primary" icon={<EditOutlined />} size="small" onClick={() => handleEditSku(record)}>
                        编辑
                      </Button>
                      <Button icon={<DollarOutlined />} size="small" onClick={() => handlePriceManagement(record)}>
                        价格管理
                      </Button>
                      <Button danger icon={<DeleteOutlined />} size="small" onClick={() => handleDeleteSku(record.id)}>
                        删除
                      </Button>
                    </Space>
                  ),
                  },
                ]}
                rowKey="id"
              />
            </Card>
            
            <Divider>SKU详情</Divider>
            
            <Card>
              <Descriptions column={2}>
                <Descriptions.Item label="商品名称">{selectedProduct.name}</Descriptions.Item>
                <Descriptions.Item label="商品ID">{selectedProduct.id}</Descriptions.Item>
                <Descriptions.Item label="分类">{selectedProduct.category?.name || ''}</Descriptions.Item>
                <Descriptions.Item label="状态">
                  <Badge 
                    status={selectedProduct.is_active ? 'success' : 'default'} 
                    text={selectedProduct.is_active ? '上架' : '下架'} 
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

      {/* 添加SKU模态框 */}
      <Modal
        title="添加SKU"
        open={isAddSkuModalOpen}
        onCancel={() => setIsAddSkuModalOpen(false)}
        footer={null}
      >
        <Form
          onFinish={handleSkuSubmit}
          layout="vertical"
        >
          <Form.Item name="sku_code" label="SKU编码" rules={[{ required: true, message: '请输入SKU编码!' }]}>
            <Input placeholder="输入SKU编码" />
          </Form.Item>
          <Form.Item name="name" label="SKU名称" rules={[{ required: true, message: '请输入SKU名称!' }]}>
            <Input placeholder="输入SKU名称" />
          </Form.Item>
          <Form.Item name="stock" label="库存" rules={[{ required: true, message: '请输入库存数量!' }]}>
            <Input type="number" placeholder="输入库存数量" />
          </Form.Item>
          <Form.Item name="cost_price" label="成本价" rules={[{ required: true, message: '请输入成本价!' }]}>
            <Input type="number" placeholder="输入成本价" />
          </Form.Item>
          <Form.Item name="weight" label="重量">
            <Input type="number" placeholder="输入重量" />
          </Form.Item>
          <Form.Item name="volume" label="体积">
            <Input type="number" placeholder="输入体积" />
          </Form.Item>
          <Form.Item name="attributes" label="SKU属性">
            <Input.TextArea rows={3} placeholder='JSON格式，例如: {"size": "M", "color": "red"}' />
          </Form.Item>
          <Form.Item name="is_active" label="状态" rules={[{ required: true, message: '请选择状态!' }]}>
            <Select>
              <Option value={true}>启用</Option>
              <Option value={false}>禁用</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsAddSkuModalOpen(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                添加
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* 编辑SKU模态框 */}
      <Modal
        title="编辑SKU"
        open={isEditSkuModalOpen}
        onCancel={() => setIsEditSkuModalOpen(false)}
        footer={null}
      >
        <Form
          initialValues={editingSku || undefined}
          onFinish={handleSkuSubmit}
          layout="vertical"
        >
          <Form.Item name="sku_code" label="SKU编码" rules={[{ required: true, message: '请输入SKU编码!' }]}>
            <Input placeholder="输入SKU编码" />
          </Form.Item>
          <Form.Item name="name" label="SKU名称" rules={[{ required: true, message: '请输入SKU名称!' }]}>
            <Input placeholder="输入SKU名称" />
          </Form.Item>
          <Form.Item name="stock" label="库存" rules={[{ required: true, message: '请输入库存数量!' }]}>
            <Input type="number" placeholder="输入库存数量" />
          </Form.Item>
          <Form.Item name="cost_price" label="成本价" rules={[{ required: true, message: '请输入成本价!' }]}>
            <Input type="number" placeholder="输入成本价" />
          </Form.Item>
          <Form.Item name="weight" label="重量">
            <Input type="number" placeholder="输入重量" />
          </Form.Item>
          <Form.Item name="volume" label="体积">
            <Input type="number" placeholder="输入体积" />
          </Form.Item>
          <Form.Item name="attributes" label="SKU属性">
            <Input.TextArea rows={3} placeholder='JSON格式，例如: {"size": "M", "color": "red"}' />
          </Form.Item>
          <Form.Item name="is_active" label="状态" rules={[{ required: true, message: '请选择状态!' }]}>
            <Select>
              <Option value={true}>启用</Option>
              <Option value={false}>禁用</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsEditSkuModalOpen(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                更新
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* 价格管理模态框 */}
      <Modal
        title={`价格管理 - ${selectedSku?.name}`}
        open={isPriceModalOpen}
        onCancel={() => setIsPriceModalOpen(false)}
        footer={null}
        width={800}
      >
        {selectedSku && (
          <Space orientation="vertical" style={{ width: '100%' }}>
            <Card>
              <Descriptions column={2}>
                <Descriptions.Item label="SKU编码">{selectedSku.sku_code}</Descriptions.Item>
                <Descriptions.Item label="SKU名称">{selectedSku.name}</Descriptions.Item>
                <Descriptions.Item label="当前库存">{selectedSku.stock}</Descriptions.Item>
                <Descriptions.Item label="成本价">¥{selectedSku.cost_price}</Descriptions.Item>
              </Descriptions>
            </Card>
            
            <Space style={{ width: '100%', justifyContent: 'space-between' }}>
              <Title level={5}>价格列表</Title>
              <Button type="primary" icon={<PlusOutlined />} onClick={handleAddPrice}>
                添加价格
              </Button>
            </Space>
            
            <Card>
              <Table 
                dataSource={selectedSku.prices || []}
                columns={[
                  { title: '价格类型', dataIndex: 'price_type', key: 'price_type' },
                  { title: '价格', dataIndex: 'price', key: 'price', render: (text) => `¥${text}` },
                  { title: '最小数量', dataIndex: 'min_quantity', key: 'min_quantity' },
                  { title: '最大数量', dataIndex: 'max_quantity', key: 'max_quantity', render: (text) => text || '无上限' },
                  { title: '状态', dataIndex: 'is_active', key: 'is_active', render: (is_active) => is_active ? '启用' : '禁用' },
                  { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
                  { 
                    title: '操作', 
                    key: 'action',
                    render: (_: any, record: any) => (
                      <Space size="middle">
                        <Button type="primary" icon={<EditOutlined />} size="small" onClick={() => handleEditPrice(record)}>
                          编辑
                        </Button>
                        <Button danger icon={<DeleteOutlined />} size="small" onClick={() => handleDeletePrice(record.id)}>
                          删除
                        </Button>
                      </Space>
                    ),
                  },
                ]}
                rowKey="id"
              />
            </Card>
            
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsPriceModalOpen(false)}>关闭</Button>
            </Space>
          </Space>
        )}
      </Modal>

      {/* 添加/编辑价格模态框 */}
      <Modal
        title={editingPrice ? '编辑价格' : '添加价格'}
        open={isAddPriceModalOpen}
        onCancel={() => setIsAddPriceModalOpen(false)}
        footer={null}
      >
        <Form
          initialValues={editingPrice || undefined}
          onFinish={handlePriceSubmit}
          layout="vertical"
        >
          <Form.Item name="price_type" label="价格类型" rules={[{ required: true, message: '请选择价格类型!' }]}>
            <Select>
              <Option value="企业价">企业价</Option>
              <Option value="渠道价">渠道价</Option>
              <Option value="终端价">终端价</Option>
              <Option value="零售价">零售价</Option>
            </Select>
          </Form.Item>
          <Form.Item name="price" label="价格" rules={[{ required: true, message: '请输入价格!' }]}>
            <Input type="number" placeholder="输入价格" />
          </Form.Item>
          <Form.Item name="min_quantity" label="最小数量" rules={[{ required: true, message: '请输入最小数量!' }]}>
            <Input type="number" placeholder="输入最小数量" />
          </Form.Item>
          <Form.Item name="max_quantity" label="最大数量">
            <Input type="number" placeholder="输入最大数量，留空表示无上限" />
          </Form.Item>
          <Form.Item name="is_active" label="状态" rules={[{ required: true, message: '请选择状态!' }]}>
            <Select>
              <Option value={true}>启用</Option>
              <Option value={false}>禁用</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsAddPriceModalOpen(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                {editingPrice ? '更新' : '添加'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

export default ProductManagement;