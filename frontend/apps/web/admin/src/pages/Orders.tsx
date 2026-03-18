import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Table, Button, Select, message } from 'antd'
import { EditOutlined } from '@ant-design/icons'
import { getOrders, updateOrderStatus } from '@/store/ordersSlice'

const { Option } = Select

const Orders = () => {
  const dispatch = useDispatch()
  const { orders, isLoading, error } = useSelector((state: any) => state.orders)

  useEffect(() => {
    dispatch(getOrders())
  }, [dispatch])

  const handleStatusChange = async (orderId: number, status: string) => {
    try {
      await dispatch(updateOrderStatus({ orderId, status })).unwrap()
      message.success('订单状态更新成功')
    } catch (err) {
      message.error('订单状态更新失败')
    }
  }

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '订单编号', dataIndex: 'order_no', key: 'order_no' },
    { title: '客户ID', dataIndex: 'customer_id', key: 'customer_id' },
    { title: '客户名称', dataIndex: 'customer_name', key: 'customer_name' },
    { title: '金额', dataIndex: 'amount', key: 'amount', render: (amount: number) => `¥${amount}` },
    { 
      title: '状态', 
      dataIndex: 'status', 
      key: 'status',
      render: (status: string, record: any) => (
        <Select 
          value={status} 
          onChange={(value) => handleStatusChange(record.id, value)}
          style={{ width: 120 }}
        >
          <Option value="pending">待支付</Option>
          <Option value="processing">处理中</Option>
          <Option value="shipped">已发货</Option>
          <Option value="completed">已完成</Option>
          <Option value="cancelled">已取消</Option>
        </Select>
      )
    },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
    { 
      title: '操作', 
      key: 'action',
      render: (_: any, record: any) => (
        <Button icon={<EditOutlined />} onClick={() => console.log('编辑订单', record.id)} />
      )
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2>订单管理</h2>
      </div>
      <Table 
        columns={columns} 
        dataSource={orders} 
        rowKey="id" 
        loading={isLoading}
        pagination={{ pageSize: 10 }}
      />
    </div>
  )
}

export { Orders }