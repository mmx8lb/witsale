import { useEffect, useState } from 'react'
import { Table, Button, Card, Row, Col, Statistic } from 'antd'
import { FieldTimeOutlined, ClockCircleOutlined, UserOutlined, EnvironmentOutlined } from '@ant-design/icons'

const FieldService = () => {
  // 模拟数据
  const fieldStaff = [
    { id: 1, name: '张三', phone: '13800138001', status: '在途', currentLocation: '北京市朝阳区', lastCheckin: '2026-03-18 10:30' },
    { id: 2, name: '李四', phone: '13900139002', status: '拜访中', currentLocation: '上海市浦东新区', lastCheckin: '2026-03-18 09:45' },
    { id: 3, name: '王五', phone: '13700137003', status: '休息', currentLocation: '广州市天河区', lastCheckin: '2026-03-18 12:00' },
    { id: 4, name: '赵六', phone: '13600136004', status: '在途', currentLocation: '深圳市南山区', lastCheckin: '2026-03-18 11:15' },
  ]

  const recentVisits = [
    { id: 1, staffName: '张三', customerName: '北京客户A', visitTime: '2026-03-18 09:00', duration: '45分钟', status: '已完成' },
    { id: 2, staffName: '李四', customerName: '上海客户B', visitTime: '2026-03-18 10:30', duration: '60分钟', status: '进行中' },
    { id: 3, name: '王五', customerName: '广州客户C', visitTime: '2026-03-18 14:00', duration: '30分钟', status: '待拜访' },
  ]

  return (
    <div>
      <h2>外勤管理</h2>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic title="外勤人员总数" value={4} prefix={<UserOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="今日拜访" value={12} prefix={<ClockCircleOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="在途人员" value={2} prefix={<FieldTimeOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="拜访中人员" value={1} prefix={<EnvironmentOutlined />} />
          </Card>
        </Col>
      </Row>

      <div style={{ marginBottom: 24 }}>
        <h3>外勤人员状态</h3>
        <Table 
          columns={[
            { title: 'ID', dataIndex: 'id', key: 'id' },
            { title: '姓名', dataIndex: 'name', key: 'name' },
            { title: '电话', dataIndex: 'phone', key: 'phone' },
            { title: '状态', dataIndex: 'status', key: 'status' },
            { title: '当前位置', dataIndex: 'currentLocation', key: 'currentLocation' },
            { title: '最后打卡', dataIndex: 'lastCheckin', key: 'lastCheckin' },
          ]}
          dataSource={fieldStaff}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </div>

      <div>
        <h3>最近拜访记录</h3>
        <Table 
          columns={[
            { title: 'ID', dataIndex: 'id', key: 'id' },
            { title: '外勤人员', dataIndex: 'staffName' || 'name', key: 'staffName' },
            { title: '客户名称', dataIndex: 'customerName', key: 'customerName' },
            { title: '拜访时间', dataIndex: 'visitTime', key: 'visitTime' },
            { title: '拜访时长', dataIndex: 'duration', key: 'duration' },
            { title: '状态', dataIndex: 'status', key: 'status' },
          ]}
          dataSource={recentVisits}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </div>
    </div>
  )
}

export { FieldService }