import { Card, Table, Button, Space, Input, Select, Typography, message, Modal, Form, InputNumber, Progress, Badge, Descriptions, Divider } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined, 
  SearchOutlined,
  InboxOutlined
} from '@ant-design/icons';
import { useState, useEffect } from 'react';
import inventoryService from '../services/inventoryService';
import { Inventory, Warehouse, InventoryMovement } from '../types';

const { Option } = Select;
const { Title, Text } = Typography;

function InventoryManagement() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Inventory | null>(null);
  const [isMovementModalOpen, setIsMovementModalOpen] = useState(false);
  const [selectedInventory, setSelectedInventory] = useState<Inventory | null>(null);
  const [warehouseData, setWarehouseData] = useState<Warehouse[]>([]);
  const [inventoryData, setInventoryData] = useState<Inventory[]>([]);
  const [movementData, setMovementData] = useState<InventoryMovement[]>([]);
  const [loading, setLoading] = useState(true);
  
  // 加载仓库数据
  useEffect(() => {
    const loadWarehouses = async () => {
      try {
        const response = await inventoryService.getWarehouses();
        setWarehouseData(response.data || []);
      } catch (error: any) {
        console.error('加载仓库数据失败:', error);
      }
    };
    
    loadWarehouses();
  }, []);
  
  // 加载库存数据
  useEffect(() => {
    const loadInventory = async () => {
      try {
        setLoading(true);
        const response = await inventoryService.getInventory();
        setInventoryData(response.data || []);
      } catch (error: any) {
        console.error('加载库存数据失败:', error);
        message.error('加载库存数据失败');
      } finally {
        setLoading(false);
      }
    };
    
    loadInventory();
  }, []);
  
  // 加载库存变动数据
  useEffect(() => {
    const loadMovements = async () => {
      try {
        const response = await inventoryService.getMovements();
        setMovementData(response.data || []);
      } catch (error: any) {
        console.error('加载库存变动数据失败:', error);
      }
    };
    
    loadMovements();
  }, []);


  const columns = [
    { title: '库存ID', dataIndex: 'id', key: 'id' },
    { title: '商品名称', dataIndex: 'product_name', key: 'product_name' },
    { title: 'SKU编码', dataIndex: 'sku_code', key: 'sku_code' },
    { title: 'SKU名称', dataIndex: 'sku_name', key: 'sku_name' },
    { title: '仓库', dataIndex: 'warehouse_name', key: 'warehouse_name' },
    { 
      title: '库存数量', 
      dataIndex: 'quantity', 
      key: 'quantity',
      render: (text: number, record: Inventory) => (
        <Space orientation="vertical">
          <Text>{text}</Text>
          <Progress 
            percent={(text / (record.threshold * 2)) * 100} 
            status={text < record.threshold ? 'exception' : 'success'} 
            size="small"
          />
        </Space>
      )
    },
    { title: '已预留', dataIndex: 'reserved_quantity', key: 'reserved_quantity' },
    { title: '预警阈值', dataIndex: 'threshold', key: 'threshold' },
    { 
      title: '状态', 
      dataIndex: 'status', 
      key: 'status',
      render: (text: string) => (
        <Badge 
          status={text === '正常' ? 'success' : 'error'} 
          text={text} 
        />
      )
    },
    { title: '更新时间', dataIndex: 'updated_at', key: 'updated_at' },
    { 
      title: '操作', 
      key: 'action', 
      render: (_: any, record: Inventory) => (
        <Space size="middle">
          <Button type="primary" icon={<EditOutlined />} size="small" onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Button icon={<InboxOutlined />} size="small" onClick={() => handleMovement(record)}>
            库存变动
          </Button>
          <Button danger icon={<DeleteOutlined />} size="small" onClick={() => handleDelete(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];

  const handleAdd = () => {
    setEditingItem(null);
    setIsModalOpen(true);
  };

  const handleEdit = (item: Inventory) => {
    setEditingItem(item);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    try {
      // 暂时使用模拟数据，实际项目中应该调用删除API
      message.success(`删除库存记录 ID: ${id} 成功`);
      // 重新加载库存数据
      const response = await inventoryService.getInventory();
      setInventoryData(response.data || []);
    } catch (error: any) {
      console.error('删除库存记录失败:', error);
      message.error('删除库存记录失败');
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      if (editingItem) {
        // 暂时使用模拟数据，实际项目中应该调用更新API
        message.success(`更新库存记录: ${values.sku_name} 成功`);
      } else {
        // 暂时使用模拟数据，实际项目中应该调用创建API
        message.success(`添加库存记录: ${values.sku_name} 成功`);
      }
      setIsModalOpen(false);
      // 重新加载库存数据
      const response = await inventoryService.getInventory();
      setInventoryData(response.data || []);
    } catch (error: any) {
      console.error('保存库存记录失败:', error);
      message.error('保存库存记录失败');
    }
  };
  
  const handleMovement = async (inventory: Inventory) => {
    try {
      // 加载库存变动数据
      const response = await inventoryService.getMovements({ sku_id: inventory.sku_id });
      setMovementData(response.data || []);
      setSelectedInventory(inventory);
      setIsMovementModalOpen(true);
    } catch (error: any) {
      console.error('加载库存变动数据失败:', error);
      message.error('加载库存变动数据失败');
      // 即使失败也打开模态框，使用基本信息
      setSelectedInventory(inventory);
      setIsMovementModalOpen(true);
    }
  };

  return (
    <div>
      <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
        <Title level={4}>库存管理</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          添加库存
        </Button>
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
              <Option value="正常">正常</Option>
              <Option value="预警">预警</Option>
            </Select>
          </Space>
          <Button>导出</Button>
        </Space>
        
        <Table dataSource={inventoryData} columns={columns} loading={loading} />
      </Card>
      
      <Modal
        title={editingItem ? '编辑库存' : '添加库存'}
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form
          initialValues={editingItem || undefined}
          onFinish={handleSubmit}
          layout="vertical"
        >
          <Form.Item name="sku_code" label="SKU编码" rules={[{ required: true, message: '请输入SKU编码!' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="sku_name" label="SKU名称" rules={[{ required: true, message: '请输入SKU名称!' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="product_name" label="商品名称" rules={[{ required: true, message: '请输入商品名称!' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="warehouse_id" label="仓库" rules={[{ required: true, message: '请选择仓库!' }]}>
            <Select>
              {warehouseData.map(warehouse => (
                <Option key={warehouse.id} value={warehouse.id}>{warehouse.name}</Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="quantity" label="库存数量" rules={[{ required: true, message: '请输入库存数量!' }]}>
            <InputNumber style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="reserved_quantity" label="已预留数量">
            <InputNumber style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="threshold" label="预警阈值" rules={[{ required: true, message: '请输入预警阈值!' }]}>
            <InputNumber style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item>
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsModalOpen(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                {editingItem ? '更新' : '添加'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
      
      {/* 库存变动模态框 */}
      <Modal
        title={`库存变动 - ${selectedInventory?.sku_name}`}
        open={isMovementModalOpen}
        onCancel={() => setIsMovementModalOpen(false)}
        footer={null}
        width={600}
      >
        {selectedInventory && (
          <Space orientation="vertical" style={{ width: '100%' }}>
            <Card>
              <Descriptions column={2}>
                <Descriptions.Item label="商品名称">{selectedInventory.product_name}</Descriptions.Item>
                <Descriptions.Item label="SKU编码">{selectedInventory.sku_code}</Descriptions.Item>
                <Descriptions.Item label="SKU名称">{selectedInventory.sku_name}</Descriptions.Item>
                <Descriptions.Item label="当前仓库">{selectedInventory.warehouse_name}</Descriptions.Item>
                <Descriptions.Item label="当前库存">{selectedInventory.quantity}</Descriptions.Item>
                <Descriptions.Item label="已预留">{selectedInventory.reserved_quantity}</Descriptions.Item>
              </Descriptions>
            </Card>
            
            <Card title="库存变动">
              <Form layout="vertical">
                <Form.Item name="type" label="变动类型" rules={[{ required: true, message: '请选择变动类型!' }]}>
                  <Select>
                    <Option value="入库">入库</Option>
                    <Option value="出库">出库</Option>
                    <Option value="调拨">调拨</Option>
                  </Select>
                </Form.Item>
                <Form.Item name="quantity" label="变动数量" rules={[{ required: true, message: '请输入变动数量!' }]}>
                  <InputNumber style={{ width: '100%' }} />
                </Form.Item>
                <Form.Item name="to_warehouse" label="目标仓库" dependencies={['type']}>
                  <Select placeholder="选择目标仓库">
                    {warehouseData.map(warehouse => (
                      <Option key={warehouse.id} value={warehouse.id}>{warehouse.name}</Option>
                    ))}
                  </Select>
                </Form.Item>
                <Form.Item name="reference" label="参考单据">
                  <Input placeholder="例如：采购单、订单号等" />
                </Form.Item>
                <Form.Item name="notes" label="备注">
                  <Input.TextArea rows={3} />
                </Form.Item>
                <Form.Item>
                  <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
                    <Button onClick={() => setIsMovementModalOpen(false)}>取消</Button>
                    <Button type="primary" htmlType="submit">
                      确认变动
                    </Button>
                  </Space>
                </Form.Item>
              </Form>
            </Card>
            
            <Divider>最近变动记录</Divider>
            
            <Card>
              <Table 
                dataSource={movementData}
                columns={[
                  { title: '变动ID', dataIndex: 'id', key: 'id' },
                  { title: '类型', dataIndex: 'type', key: 'type' },
                  { title: '数量', dataIndex: 'quantity', key: 'quantity' },
                  { title: '仓库', dataIndex: 'warehouse', key: 'warehouse' },
                  { title: '来源仓库', dataIndex: 'from_warehouse', key: 'from_warehouse' },
                  { title: '目标仓库', dataIndex: 'to_warehouse', key: 'to_warehouse' },
                  { title: '参考单据', dataIndex: 'reference', key: 'reference' },
                  { title: '变动时间', dataIndex: 'created_at', key: 'created_at' },
                ]}
                pagination={false}
              />
            </Card>
          </Space>
        )}
      </Modal>
    </div>
  );
}

export default InventoryManagement;