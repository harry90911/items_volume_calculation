def sort_item(order_sku_list):
	
	order_sku_list_rearrange = list()
	for order_sku_info_list in order_sku_list:
		quantity = order_sku_info_list[5]
		volume = order_sku_info_list[2] * order_sku_info_list[3] * order_sku_info_list[4]
		order_sku_info_list[5] = volume
		for i in range(0, quantity):
			order_sku_list_rearrange.append(order_sku_info_list)

	sorted_sku_list = sorted(order_sku_list_rearrange, key=lambda sku_info_list:sku_info_list[5], reverse=True)

	return sorted_sku_list


def calculate_volume_and_comparison(placed_point_list,reference_line_list,sorted_order_sku_info_list):

	x = sorted_order_sku_info_list[2]
	y = sorted_order_sku_info_list[3]
	z = sorted_order_sku_info_list[4]
	rotations = [[x,y,z],[y,x,z],[x,z,y],[z,x,y],[y,z,x],[z,y,x]]
	all_selections = list()
	for placed_point in placed_point_list:
		for rotation in rotations:
			volume_x = reference_line_list[0]
			volume_y = reference_line_list[1]
			volume_z = reference_line_list[2]
			# x,y,z 參考線
			reference_line_output = [reference_line_list[0],
									 reference_line_list[1],
									 reference_line_list[2]]
			# 放置點加上立方體長/寬/高
			for_reference_line_list = [(placed_point[0] + rotation[0]),
									   (placed_point[1] + rotation[1]),
									   (placed_point[2] + rotation[2])]
			if for_reference_line_list[0] >= reference_line_list[0]:
				volume_x = for_reference_line_list[0]
				reference_line_output[0] = for_reference_line_list[0]
			if for_reference_line_list[1] >= reference_line_list[1]:
				volume_y = for_reference_line_list[1]
				reference_line_output[1] = for_reference_line_list[1]
			if for_reference_line_list[2] >= reference_line_list[2]:
				volume_z = for_reference_line_list[2]
				reference_line_output[2] = for_reference_line_list[2]
			# 計算體積
			volume = volume_x*volume_y*volume_z
			# 計算長寬高加總
			line_sum = sum(reference_line_output)

			# 新增放置點
			placed_point_1 = [for_reference_line_list[0],placed_point[1],placed_point[2]]
			placed_point_2 = [placed_point[0],for_reference_line_list[1],placed_point[2]]
			placed_point_3 = [placed_point[0],placed_point[1],for_reference_line_list[2]]
			all_selections.append([volume, placed_point_1, placed_point_2, placed_point_3, placed_point, reference_line_output, line_sum])

	# 取最小加總
	lowest_line_sum = sorted(all_selections, key=lambda info_list:info_list[6])[0][6]
	choices = [selection for selection in all_selections if selection[6] == lowest_line_sum]

	# 取最小體積
	lowest_volume = sorted(choices, key=lambda info_list:info_list[0])[0][0]
	best_choice = [selection for selection in choices if selection[0] == lowest_volume][0]
	
	placed_point_list_output = placed_point_list
	# 放置點變更，少1個，加3個
	placed_point_list_output.append(best_choice[1])
	placed_point_list_output.append(best_choice[2])
	placed_point_list_output.append(best_choice[3])
	placed_point_list_output.remove(best_choice[4])
	# 參考線更新
	reference_line_output = best_choice[5]
	# 商品總體積
	volume = best_choice[0]

	return [placed_point_list_output,reference_line_output,volume]


def calculate_volume(sorted_order_sku_list):
	
	sku_count = len(sorted_order_sku_list)
	ordersn = sorted_order_sku_list[0][0]
	x = sorted_order_sku_list[0][2]
	y = sorted_order_sku_list[0][3]
	z = sorted_order_sku_list[0][4]
	box_number = sorted_order_sku_list[0][6]
	box_volume = sorted_order_sku_list[0][7]
	order_type = sorted_order_sku_list[0][8]
	created_at = sorted_order_sku_list[0][9]

	output_dict = dict()
	if len(sorted_order_sku_list)>1:
		rotations = [[x,y,z],[y,x,z],[z,x,y],[x,z,y],[z,y,x],[y,z,x]]
		rotation_output = list()
		for rotation in rotations:
			reference_line_list = [rotation[0],rotation[1],rotation[2]]
			placed_point_list = [[rotation[0],0,0],[0,rotation[1],0],[0,0,rotation[2]]]
			for sorted_order_sku_info_list in sorted_order_sku_list[1:]:
				# 搜尋一個新立方體在所有放置點的最佳位置和體積
				info_list = calculate_volume_and_comparison(placed_point_list,reference_line_list,sorted_order_sku_info_list)
				placed_point_list = info_list[0]
				reference_line_list = info_list[1]
				volume = info_list[2]
				line_sum = sum(info_list[1])
			rotation_output.append([volume,placed_point_list,reference_line_list,line_sum])

		lowest_line_sum = sorted(rotation_output, key=lambda x: x[3])[0][3]
		choices = [selection for selection in rotation_output if selection[3] == lowest_line_sum]
		lowest_volume = sorted(choices, key=lambda info_list:info_list[0])[0][0]
		best_choice = [selection for selection in choices if selection[0] == lowest_volume][0]
		best_choice[2] = sorted(best_choice[2])
		volume = (best_choice[2][0]*1.05+1.5)*(best_choice[2][1]*1.05+1.5)*(best_choice[2][2]*1.05+1.5)
		output_dict = {
			'ordersn':ordersn,
			'sku_count': sku_count,
			'volume':volume,
			# 'placed_point_list':best_choice[1],
			'length':best_choice[2][0]*1.05+1.5,
			'width':best_choice[2][1]*1.05+1.5,
			'height':best_choice[2][2]*1.05+1.5,
			'box_number':box_number,
			'box_volume':box_volume,
			'utilization':volume/box_volume,
			'order_type':order_type,
			'created_at':created_at}

	else:
		volume = (x*1.05+1.5)*(y*1.05+1.5)*(z*1.05+1.5)
		sorted_lst = sorted([x,y,z])
		output_dict = {
			'ordersn':ordersn,
			'sku_count': sku_count,
			'volume':volume,
			# 'placed_point_list':[[x,0,0],[0,y,0],[0,0,z]],
			'length':sorted_lst[0]*1.05+1.5,
			'width':sorted_lst[1]*1.05+1.5,
			'height':sorted_lst[2]*1.05+1.5,
			'box_number':box_number,
			'box_volume':box_volume,
			'utilization':volume/box_volume,
			'order_type':order_type,
			'created_at':created_at}

	return output_dict

if __name__ == '__main__':
	# Example
	# [shopee_order_sn, sku_id, 長, 寬, 高]
	order_sku_list = [['123xx','aaa',1,30,47,1,'SP-105'],
					    ['123xx','aaa',1,8,31,1,'SP-105']]
	# 物品由大到小排列
	sorted_order_sku_list = sort_item(order_sku_list)
	# 進行計算
	volume_info = calculate_volume(sorted_order_sku_list)