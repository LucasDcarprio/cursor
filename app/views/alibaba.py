"""
阿里巴巴集成视图模块
Alibaba Integration Views Module

处理与阿里巴巴平台的集成功能。
"""

from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from alibaba_api import (
    get_skuinfo, get_skuinfo_detail, make_order, 
    bulk_order, check_payment, get_order_list, get_wuliu
)
import json

alibaba_bp = Blueprint('alibaba', __name__)

@alibaba_bp.route('/product/<int:product_id>')
@login_required
def get_product_info(product_id):
    """获取商品信息"""
    try:
        sku_infos = get_skuinfo_detail(product_id, user_id=current_user.id)
        
        if not sku_infos:
            return jsonify({
                'success': False,
                'message': f'未找到商品ID {product_id} 的信息'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'product_id': product_id,
                'sku_infos': sku_infos
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取商品信息失败: {str(e)}'
        }), 500

@alibaba_bp.route('/order/create', methods=['POST'])
@login_required
def create_order():
    """创建阿里巴巴订单"""
    try:
        data = request.get_json()
        
        if not data or not data.get('items'):
            return jsonify({
                'success': False,
                'message': '订单项目不能为空'
            }), 400
        
        store_id = data.get('store_id')
        items = data.get('items')
        
        # 调用阿里巴巴下单API
        result = make_order(items, user_id=current_user.id, store_id=store_id)
        
        if result and result.startswith("success:"):
            order_id = result.split(":")[1]
            return jsonify({
                'success': True,
                'message': '订单创建成功',
                'order_id': order_id
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'订单创建失败: {result}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建订单时发生错误: {str(e)}'
        }), 500

@alibaba_bp.route('/order/bulk', methods=['POST'])
@login_required
def bulk_create_orders():
    """批量下单"""
    try:
        data = request.get_json()
        store_id = data.get('store_id') if data else None
        
        # 调用批量下单函数
        bulk_order(user_id=current_user.id, store_id=store_id)
        
        return jsonify({
            'success': True,
            'message': '批量下单任务已启动'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'批量下单失败: {str(e)}'
        }), 500

@alibaba_bp.route('/payment/check', methods=['POST'])
@login_required
def check_order_payment():
    """检查订单支付状态"""
    try:
        data = request.get_json()
        store_id = data.get('store_id') if data else None
        
        # 调用支付检查函数
        result = check_payment(user_id=current_user.id, store_id=store_id)
        
        return jsonify({
            'success': True,
            'message': '支付状态检查完成',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'检查支付状态失败: {str(e)}'
        }), 500

@alibaba_bp.route('/orders')
@login_required
def get_alibaba_orders():
    """获取阿里巴巴订单列表"""
    try:
        # 获取查询参数
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        status = request.args.get('status')
        store_id = request.args.get('store_id')
        
        # 调用阿里巴巴订单查询API
        result = get_order_list(
            start_time=start_time,
            end_time=end_time,
            status=status,
            user_id=current_user.id,
            store_id=store_id
        )
        
        if isinstance(result, dict) and 'orders' in result:
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': '获取订单列表失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取订单列表失败: {str(e)}'
        }), 500

@alibaba_bp.route('/logistics/<order_id>')
@login_required
def get_logistics_info(order_id):
    """获取物流信息"""
    try:
        store_id = request.args.get('store_id')
        
        # 调用物流查询API
        logistics_info = get_wuliu(order_id, user_id=current_user.id, store_id=store_id)
        
        if logistics_info:
            return jsonify({
                'success': True,
                'data': logistics_info
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'未找到订单 {order_id} 的物流信息'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取物流信息失败: {str(e)}'
        }), 500

@alibaba_bp.route('/config')
@login_required
def alibaba_config():
    """阿里巴巴配置页面"""
    return render_template('alibaba/config.html')

@alibaba_bp.route('/orders/management')
@login_required
def order_management():
    """订单管理页面"""
    return render_template('alibaba/orders.html')