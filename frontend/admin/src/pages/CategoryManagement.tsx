import { Card, Table, Button, Space, Input, Select, Typography, message, Modal, Form, TreeSelect, Popconfirm, Switch } from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  SearchOutlined,
  UploadOutlined,
  DownloadOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  FilterOutlined
} from '@ant-design/icons';
import { useState, useEffect } from 'react';
import productService from '../services/productService';
import { Category } from '../types';

const { Option } = Select;
const { Title, Text } = Typography;

function CategoryManagement() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);
  const [categoryData, setCategoryData] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchText, setSearchText] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [sortOrder, setSortOrder] = useState('ascend');
  const [sortField, setSortField] = useState('sortOrder');
  
  // 加载分类数据
  const loadCategories = async () => {
    try {
      setLoading(true);
      const response = await productService.getCategories();
      const categories: any[] = response.data || [];
      // 转换分类数据，确保每个节点都有有效的value和title
      const transformedCategories = categories.map(category => ({
        title: category.name || '未命名分类',
        value: category.id.toString(),
        status: category.is_active ? 'active' : 'inactive',
        sortOrder: category.sort || 0,
        parentId: category.parent_id ? category.parent_id.toString() : null,
        children: []
      }));
      
      // 构建树形结构
      const buildTree = (categories: any[], parentId: string | null = null): any[] => {
        return categories
          .filter(category => category.parentId === parentId)
          .map(category => ({
            ...category,
            children: buildTree(categories, category.value)
          }));
      };
      
      const treeData = buildTree(transformedCategories);
      setCategoryData(treeData);
    } catch (error: any) {
      console.error('加载分类数据失败:', error);
      message.error('加载分类数据失败');
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    loadCategories();
  }, []);
  
  // 处理添加分类
  const handleAdd = () => {
    setEditingCategory(null);
    setIsModalOpen(true);
  };
  
  // 处理编辑分类
  const handleEdit = (category: Category) => {
    setEditingCategory(category);
    setIsModalOpen(true);
  };
  
  // 处理删除分类
  const handleDelete = async (id: string) => {
    try {
      await productService.deleteCategory(id);
      message.success(`删除分类 ID: ${id} 成功`);
      loadCategories();
    } catch (error: any) {
      console.error('删除分类失败:', error);
      message.error('删除分类失败');
    }
  };
  
  // 处理提交分类
  const handleSubmit = async (values: any) => {
    try {
      // 转换数据格式，使用后端需要的字段名
      const categoryData = {
        name: values.name,
        parent_id: values.parentId || null,
        sort: values.sortOrder || 0,
        level: values.parentId ? 2 : 1
      };
      
      if (editingCategory) {
        await productService.updateCategory(editingCategory.value, categoryData);
        message.success(`更新分类: ${values.name} 成功`);
      } else {
        await productService.createCategory(categoryData);
        message.success(`添加分类: ${values.name} 成功`);
      }
      setIsModalOpen(false);
      loadCategories();
    } catch (error: any) {
      console.error('保存分类失败:', error);
      message.error('保存分类失败');
    }
  };
  
  // 处理状态切换
  const handleStatusChange = async (id: string, checked: boolean) => {
    try {
      await productService.updateCategory(id, { is_active: checked });
      message.success(`分类状态更新成功`);
      loadCategories();
    } catch (error: any) {
      console.error('更新分类状态失败:', error);
      message.error('更新分类状态失败');
    }
  };
  
  // 处理排序
  const handleSort = (_categoryId: string, _direction: 'up' | 'down') => {
    // 实现排序逻辑
    message.info('排序功能开发中');
  };
  
  // 处理导入
  const handleImport = () => {
    message.info('导入功能开发中');
  };
  
  // 处理导出
  const handleExport = () => {
    message.info('导出功能开发中');
  };
  
  // 转换为扁平数据结构用于表格展示
  const flattenCategories = (categories: any[], parentName: string = '无'): any[] => {
    let result: any[] = [];
    categories.forEach(category => {
      result.push({
        key: category.value,
        id: category.value,
        name: category.title,
        parent: parentName,
        level: category.parentId ? 2 : 1,
        sortOrder: category.sortOrder,
        status: category.status
      });
      if (category.children && category.children.length > 0) {
        result = result.concat(flattenCategories(category.children, category.title));
      }
    });
    return result;
  };
  
  // 过滤和排序数据
  const filteredData = flattenCategories(categoryData)
    .filter(item => {
      const matchesSearch = item.name.toLowerCase().includes(searchText.toLowerCase());
      const matchesStatus = statusFilter ? item.status === statusFilter : true;
      return matchesSearch && matchesStatus;
    })
    .sort((a, b) => {
      if (sortOrder === 'ascend') {
        return a[sortField as keyof typeof a] > b[sortField as keyof typeof b] ? 1 : -1;
      } else {
        return a[sortField as keyof typeof a] < b[sortField as keyof typeof b] ? 1 : -1;
      }
    });
  
  const columns = [
    {
      title: '分类ID',
      dataIndex: 'id',
      key: 'id',
      sorter: true,
      sortOrder: sortField === 'id' ? sortOrder as any : false,
      onHeaderCell: (_column: any) => ({
        onClick: () => setSortField('id')
      })
    },
    {
      title: '分类名称',
      dataIndex: 'name',
      key: 'name',
      sorter: true,
      sortOrder: sortField === 'name' ? sortOrder as any : false,
      onHeaderCell: (_column: any) => ({
        onClick: () => setSortField('name')
      })
    },
    {
      title: '父分类',
      dataIndex: 'parent',
      key: 'parent'
    },
    {
      title: '层级',
      dataIndex: 'level',
      key: 'level'
    },
    {
      title: '排序',
      dataIndex: 'sortOrder',
      key: 'sortOrder',
      sorter: true,
      sortOrder: sortField === 'sortOrder' ? sortOrder as any : false,
      onHeaderCell: (_column: any) => ({
        onClick: () => setSortField('sortOrder')
      }),
      render: (text: number, record: any) => (
        <Space>
          <Button 
            icon={<ArrowUpOutlined />} 
            size="small" 
            onClick={() => handleSort(record.id, 'up')}
          />
          <Text>{text}</Text>
          <Button 
            icon={<ArrowDownOutlined />} 
            size="small" 
            onClick={() => handleSort(record.id, 'down')}
          />
        </Space>
      )
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      sorter: true,
      sortOrder: sortField === 'status' ? sortOrder as any : false,
      onHeaderCell: (_column: any) => ({
        onClick: () => setSortField('status')
      }),
      render: (text: string, record: any) => (
        <Switch
          checked={text === 'active'}
          onChange={(checked) => handleStatusChange(record.id, checked)}
        />
      )
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button type="primary" icon={<EditOutlined />} size="small" onClick={() => handleEdit({ value: record.id, title: record.name } as Category)}>
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个分类吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button danger icon={<DeleteOutlined />} size="small">
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ] as any;

  return (
    <div>
      <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
        <Title level={4}>分类管理</Title>
        <Space>
          <Button icon={<UploadOutlined />} onClick={handleImport}>
            导入
          </Button>
          <Button icon={<DownloadOutlined />} onClick={handleExport}>
            导出
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加分类
          </Button>
        </Space>
      </Space>
      
      <Card>
        <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
          <Space>
            <Input 
              placeholder="搜索分类名称" 
              prefix={<SearchOutlined />} 
              style={{ width: 200 }} 
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
            />
            <Select 
              placeholder="状态" 
              style={{ width: 120 }} 
              value={statusFilter}
              onChange={setStatusFilter}
            >
              <Option value="">全部</Option>
              <Option value="active">启用</Option>
              <Option value="inactive">禁用</Option>
            </Select>
            <Button icon={<FilterOutlined />} onClick={() => {
              setSearchText('');
              setStatusFilter('');
            }}>
              重置
            </Button>
          </Space>
        </Space>
        
        <Table 
          dataSource={filteredData} 
          columns={columns} 
          loading={loading} 
          rowKey="id" 
          onChange={(_pagination, _filters, sorter) => {
            const sortInfo = sorter as any;
            setSortOrder(sortInfo.order || 'ascend');
            setSortField(sortInfo.field as string || 'sortOrder');
          }}
        />
      </Card>
      
      <Modal
        title={editingCategory ? '编辑分类' : '添加分类'}
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form
          initialValues={editingCategory ? { name: editingCategory.title, parentId: (editingCategory as any).parentId } : undefined}
          onFinish={handleSubmit}
          layout="vertical"
        >
          <Form.Item name="name" label="分类名称" rules={[{ required: true, message: '请输入分类名称!' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="parentId" label="父分类">
            <TreeSelect
              treeData={categoryData}
              placeholder="选择父分类"
              style={{ width: '100%' }}
              treeDefaultExpandAll={true}
            />
          </Form.Item>
          <Form.Item name="sortOrder" label="排序号">
            <Input type="number" placeholder="输入排序号" />
          </Form.Item>
          <Form.Item name="status" label="状态" initialValue="active">
            <Select>
              <Option value="active">启用</Option>
              <Option value="inactive">禁用</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
              <Button onClick={() => setIsModalOpen(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                {editingCategory ? '更新' : '添加'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

export default CategoryManagement;