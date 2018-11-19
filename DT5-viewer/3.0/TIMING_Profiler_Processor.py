import os,sys

def TIMING_Profiler_Processor(path,DInt,EDInt,ContInt,TimInt,Pix):

	# Specify the Feature Table
	filename = path + 'features/Table_Exp.txt'

	print filename

	# Define the output Tables
	Cells_Master = []
	Cells_1E0T = []
	Cells_0E1T = []
	Cells_1E1T = []
	Cells_1E2T = []
	Cells_1E3T = []



	# Load and format the Feature Table
	f = open(filename,'r')

	f_txt = f.read()

	f_txt = f_txt.split('\n')

	cols = len(f_txt[0].split('\t'))
	print "cols = " + str(cols)

	rows = len(f_txt) - 1
	print "rows = " + str(rows)
	wells = rows/49

	Cells = []

	Cells_plus = []

	Cells_UID = []

	for line in range(0,rows):
		temp1 = f_txt[line].split('\t')
		Cells.append([float(i) for i in temp1])
		
		# temp2 = [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000]
		temp2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		Cells_plus.append(temp2)
		
		Cells_UID.append(0)
		
		
	# Initialize the Vars
	Kill_1_1 = 0
	Kill_1_0 = 0
	Kill_2_2 = 0
	Kill_2_1 = 0
	Kill_2_0 = 0
	Kill_3_3 = 0
	Kill_3_2 = 0
	Kill_3_1 = 0
	Kill_3_0 = 0

	Dead_1_1 = 0
	Dead_1_0 = 0
	Dead_2_2 = 0
	Dead_2_1 = 0
	Dead_2_0 = 0
	Dead_3_3 = 0
	Dead_3_2 = 0
	Dead_3_1 = 0
	Dead_3_0 = 0

	Header_Main = []
	Header_Main.append('UID')
	Header_Main.append('Block')
	Header_Main.append('X')
	Header_Main.append('Y')
	Header_Main.append('Features')
	for i in range(0,cols):
		Header_Main.append(str(i))

	# Getting Thresholds
	# DInt = 125
	# ContInt = 0.01
	# TimInt = 6
	# Pix = 0.325


	# Filling UIDs, effector, tar, total tar

	label_list_x = []
	label_list_x.append('Effector')
	label_list_x.append('Tar')
	label_list_x.append('Total Tar')
	label_list_x.append('tSeek (min)')
	label_list_x.append('tEffDeath (min)')
	label_list_x.append('Absol death (min)')
	label_list_x.append('tDeath (min)')
	label_list_x.append('tContact (min)')
	label_list_x.append('Eff dWell No cont (um)')
	label_list_x.append('EffdWell cont (um)')
	label_list_x.append('EffAR No cont')
	label_list_x.append('EffAR cont')
	label_list_x.append('Tar dWell No cont (um)')
	label_list_x.append('Tar dWell cont (um)')
	label_list_x.append('Tar AR No cont')
	label_list_x.append('Tar AR cont')

	label_list_y = []
	label_list_y.append("Time_point")
	label_list_y.append("Eff_x")
	label_list_y.append("Eff_y")
	label_list_y.append("Eff_AR")
	label_list_y.append("Eff_Speed")
	label_list_y.append("Eff_death_int")
	label_list_y.append("Eff_death")
	label_list_y.append("Tar1x")
	label_list_y.append("Tar1y")
	label_list_y.append("Target1_AR")
	label_list_y.append("Tar1_Speed")
	label_list_y.append("Tar1D_Int")
	label_list_y.append("Tar1D")
	label_list_y.append("Cont1_Int")
	label_list_y.append("Cont1")
	label_list_y.append("Tar2x")
	label_list_y.append("Tar2y")
	label_list_y.append("Target2_AR")
	label_list_y.append("Tar2_Speed")
	label_list_y.append("Tar2D_Int")
	label_list_y.append("Tar2D")
	label_list_y.append("Cont2_Int")
	label_list_y.append("Cont2")
	label_list_y.append("Tar3x")
	label_list_y.append("Tar3y")
	label_list_y.append("Target3_AR")
	label_list_y.append("Tar3_Speed")
	label_list_y.append("Tar3D_Int")
	label_list_y.append("Tar3D")
	label_list_y.append("Cont3_Int")
	label_list_y.append("Cont3")
	label_list_y.append("Tar4x")
	label_list_y.append("Tar4y")
	label_list_y.append("Target4_AR")
	label_list_y.append("Tar4_Speed")
	label_list_y.append("Tar4D_Int")
	label_list_y.append("Tar4D")
	label_list_y.append("Cont4_Int")
	label_list_y.append("Cont4")
	label_list_y.append("Tar5x")
	label_list_y.append("Tar5y")
	label_list_y.append("Target5_AR")
	label_list_y.append("Tar5_Speed")
	label_list_y.append("Tar5D_Int")
	label_list_y.append("Tar5D")
	label_list_y.append("Cont5_Int")
	label_list_y.append("Cont5")
	label_list_y.append("BEAD_I")
	label_list_y.append("BEAD_II")

	# Main Nanowell Processing Loop

	for i in range(1,wells+1):
		Effsum = 0
		Tar1sum = 0
		Tar2sum = 0
		Tar3sum = 0
		Tar4sum = 0
		Tar5sum = 0
		
		for k in range(3, cols):
			Effsum = Effsum + Cells[(i-1)*49][k]
			Tar1sum = Tar1sum + Cells[(i-1)*49+6][k]
			Tar2sum = Tar2sum + Cells[(i-1)*49+14][k]
			Tar3sum = Tar3sum + Cells[(i-1)*49+22][k]
			Tar4sum = Tar4sum + Cells[(i-1)*49+30][k]
			Tar5sum = Tar5sum + Cells[(i-1)*49+38][k]

		# Setting thresholds
		# Setting threshold for first column
		for k in range(3,cols):

			if k == 3:
				# Death THresholds for effector and 5 targets
				if Cells[(i-1)*49+4][k] >=EDInt:
					Cells[(i-1)*49+5][k] = 1
				else:
					Cells[(i-1)*49+5][k] = 0


				if Cells[(i-1)*49+10][k] >=DInt:
					Cells[(i-1)*49+11][k] = 1
				else:
					Cells[(i-1)*49+11][k] = 0


				if Cells[(i-1)*49+18][k] >=DInt:
					Cells[(i-1)*49+19][k] = 1
				else:
					Cells[(i-1)*49+19][k] = 0


				if Cells[(i-1)*49+26][k] >=DInt:
					Cells[(i-1)*49+27][k] = 1
				else:
					Cells[(i-1)*49+27][k] = 0


				if Cells[(i-1)*49+34][k] >=DInt:
					Cells[(i-1)*49+35][k] = 1
				else:
					Cells[(i-1)*49+35][k] = 0


				if Cells[(i-1)*49+42][k] >=DInt:
					Cells[(i-1)*49+43][k] = 1
				else:
					Cells[(i-1)*49+43][k] = 0
					
					
				# Contact Thresholds
				
				if Effsum > -40000:
					if Tar1sum > -40000:
						if Cells[(i-1)*49+12][k] >= ContInt:
							if Cells[(i-1)*49+12][k+1] >= ContInt:
								Cells[(i-1)*49+13][k] = 1
							else:
								Cells[(i-1)*49+13][k] = 0
						else:
							Cells[(i-1)*49+13][k] = 0
					else:
						Cells[(i-1)*49+13][k] = 0


					if Tar2sum > -40000:
						if Cells[(i-1)*49+20][k] >= ContInt and Cells[(i-1)*49+20][k+1] >= ContInt:
							Cells[(i-1)*49+21][k] = 1
						else:
							Cells[(i-1)*49+21][k] = 0
					else:
						Cells[(i-1)*49+21][k] = 0

					if Tar3sum > -40000:
						if Cells[(i-1)*49+28][k] >= ContInt and Cells[(i-1)*49+28][k+1] >= ContInt:
							Cells[(i-1)*49+29][k] = 1
						else:
							Cells[(i-1)*49+29][k] = 0
					else:
						Cells[(i-1)*49+29][k] = 0


					if Tar4sum > -40000:
						if Cells[(i-1)*49+36][k] >= ContInt and Cells[(i-1)*49+36][k+1] >= ContInt:
							Cells[(i-1)*49+37][k] = 1
						else:
							Cells[(i-1)*49+37][k] = 0
					else:
						Cells[(i-1)*49+37][k] = 0


					if Tar5sum > -40000:
						if Cells[(i-1)*49+44][k] >= ContInt and Cells[(i-1)*49+44][k+1] >= ContInt:
							Cells[(i-1)*49+45][k] = 1
						else:
							Cells[(i-1)*49+45][k] = 0
					else:
						Cells[(i-1)*49+45][k] = 0
						
				else:
					# No Effectors
					Cells[(i-1)*49+13][k] = 0
					Cells[(i-1)*49+21][k] = 0
					Cells[(i-1)*49+29][k] = 0
					Cells[(i-1)*49+37][k] = 0
					Cells[(i-1)*49+45][k] = 0
					
			else: # for k > 3
				
				# Death Thresholds
				if Cells[(i-1)*49+5][k-1] == 1:
					Cells[(i-1)*49+5][k] = 1
				elif Cells[(i-1)*49+4][k] >= EDInt:
					Cells[(i-1)*49+5][k] = 1
				else:
					Cells[(i-1)*49+5][k] = 0

				if Cells[(i-1)*49+11][k-1] == 1:
					Cells[(i-1)*49+11][k] = 1
				elif Cells[(i-1)*49+10][k] >= DInt:
					Cells[(i-1)*49+11][k] = 1
				else:
					Cells[(i-1)*49+11][k] = 0


				if Cells[(i-1)*49+19][k-1] == 1:
					Cells[(i-1)*49+19][k] = 1
				elif Cells[(i-1)*49+18][k] >= DInt:
					Cells[(i-1)*49+19][k] = 1
				else:
					Cells[(i-1)*49+19][k] = 0


				if Cells[(i-1)*49+27][k-1] == 1:
					Cells[(i-1)*49+27][k] = 1
				elif Cells[(i-1)*49+26][k] >= DInt:
					Cells[(i-1)*49+27][k] = 1
				else:
					Cells[(i-1)*49+27][k] = 0


				if Cells[(i-1)*49+35][k-1] == 1:
					Cells[(i-1)*49+35][k] = 1
				elif Cells[(i-1)*49+34][k] >= DInt:
					Cells[(i-1)*49+35][k] = 1
				else:
					Cells[(i-1)*49+35][k] = 0
					
				if Cells[(i-1)*49+43][k-1] == 1:
					Cells[(i-1)*49+43][k] = 1
				elif Cells[(i-1)*49+42][k] >= DInt:
					Cells[(i-1)*49+43][k] = 1
				else:
					Cells[(i-1)*49+43][k] = 0
					
					
				# Contact Thresholds
				if k < cols-1:
					if Effsum > -40000:
						
						if Tar1sum > -40000:
							if (Cells[(i-1)*49+12][k] >= ContInt and Cells[(i-1)*49+12][k-1] >= ContInt) or Cells[(i-1)*49+12][k+1] >= ContInt:
								Cells[(i-1)*49+13][k] = 1
							elif Cells[(i-1)*49+12][k-1] >= ContInt and Cells[(i-1)*49+12][k+1] >= ContInt:
								Cells[(i-1)*49+13][k] = 1
							else:
								Cells[(i-1)*49+13][k] = 0
						else:
							Cells[(i-1)*49+13][k] = 0

						if Tar2sum > -40000:
							if (Cells[(i-1)*49+20][k] >= ContInt and Cells[(i-1)*49+20][k-1] >= ContInt) or Cells[(i-1)*49+20][k+1] >= ContInt:
								Cells[(i-1)*49+21][k] = 1
							elif Cells[(i-1)*49+20][k-1] >= ContInt and Cells[(i-1)*49+20][k+1] >= ContInt:
								Cells[(i-1)*49+21][k] = 1
							else:
								Cells[(i-1)*49+21][k] = 0
						else:
							Cells[(i-1)*49+21][k] = 0

						if Tar3sum > -40000:
							if (Cells[(i-1)*49+28][k] >= ContInt and Cells[(i-1)*49+28][k-1] >= ContInt) or Cells[(i-1)*49+28][k+1] >= ContInt:
								Cells[(i-1)*49+29][k] = 1
							elif Cells[(i-1)*49+28][k-1] >= ContInt and Cells[(i-1)*49+28][k+1] >= ContInt:
								Cells[(i-1)*49+29][k] = 1
							else:
								Cells[(i-1)*49+29][k] = 0
						else:
							Cells[(i-1)*49+29][k] = 0

						if Tar4sum > -40000:
							if (Cells[(i-1)*49+36][k] >= ContInt and Cells[(i-1)*49+36][k-1] >= ContInt) or Cells[(i-1)*49+36][k+1] >= ContInt:
								Cells[(i-1)*49+37][k] = 1
							elif Cells[(i-1)*49+36][k-1] >= ContInt and Cells[(i-1)*49+36][k+1] >= ContInt:
								Cells[(i-1)*49+37][k] = 1
							else:
								Cells[(i-1)*49+37][k] = 0
						else:
							Cells[(i-1)*49+37][k] = 0

						if Tar5sum > -40000:
							if (Cells[(i-1)*49+44][k] >= ContInt and Cells[(i-1)*49+44][k-1] >= ContInt) or Cells[(i-1)*49+44][k+1] >= ContInt:
								Cells[(i-1)*49+45][k] = 1
							elif Cells[(i-1)*49+44][k-1] >= ContInt and Cells[(i-1)*49+44][k+1] >= ContInt:
								Cells[(i-1)*49+45][k] = 1
							else:
								Cells[(i-1)*49+45][k] = 0
						else:
							Cells[(i-1)*49+45][k] = 0

					else:
						Cells[(i-1)*49+13][k] = 0
						Cells[(i-1)*49+21][k] = 0
						Cells[(i-1)*49+29][k] = 0
						Cells[(i-1)*49+37][k] = 0
						Cells[(i-1)*49+45][k] = 0
						
				else: # k = cols-1
					if Effsum > -40000:
						
						if Tar1sum > -40000:
							if Cells[(i-1)*49+12][k] >= ContInt and Cells[(i-1)*49+12][k-1] >= ContInt:
								Cells[(i-1)*49+13][k] = 1
							else:
								Cells[(i-1)*49+13][k] = 0
						else:
							Cells[(i-1)*49+13][k] = 0

						if Tar2sum > -40000:
							if Cells[(i-1)*49+20][k] >= ContInt and Cells[(i-1)*49+20][k-1] >= ContInt:
								Cells[(i-1)*49+21][k] = 1
							else:
								Cells[(i-1)*49+21][k] = 0
						else:
							Cells[(i-1)*49+21][k] = 0

						if Tar3sum > -40000:
							if Cells[(i-1)*49+28][k] >= ContInt and Cells[(i-1)*49+28][k-1] >= ContInt:
								Cells[(i-1)*49+29][k] = 1
							else:
								Cells[(i-1)*49+29][k] = 0
						else:
							Cells[(i-1)*49+29][k] = 0

						if Tar4sum > -40000:
							if Cells[(i-1)*49+36][k] >= ContInt and Cells[(i-1)*49+36][k-1] >= ContInt:
								Cells[(i-1)*49+37][k] = 1
							else:
								Cells[(i-1)*49+37][k] = 0
						else:
							Cells[(i-1)*49+37][k] = 0

						if Tar5sum > -40000:
							if Cells[(i-1)*49+44][k] >= ContInt and Cells[(i-1)*49+44][k-1] >= ContInt:
								Cells[(i-1)*49+45][k] = 1
							else:
								Cells[(i-1)*49+45][k] = 0
						else:
							Cells[(i-1)*49+45][k] = 0

					else:
						Cells[(i-1)*49+13][k] = 0
						Cells[(i-1)*49+21][k] = 0
						Cells[(i-1)*49+29][k] = 0
						Cells[(i-1)*49+37][k] = 0
						Cells[(i-1)*49+45][k] = 0


						
		# Determine if contact exists
		
		SumContT1 = 0
		SumContT2 = 0
		SumContT3 = 0
		SumContT4 = 0
		SumContT5 = 0
		SumD1 = 0
		SumD2 = 0
		SumD3 = 0
		SumD4 = 0
		SumD5 = 0
		SumD6 = 0
		
		for k in range(3,cols):
			SumContT1 = SumContT1 + Cells[(i-1)*49+13][k]
			SumContT2 = SumContT2 + Cells[(i-1)*49+21][k]
			SumContT3 = SumContT3 + Cells[(i-1)*49+29][k]
			SumContT4 = SumContT4 + Cells[(i-1)*49+37][k]
			SumContT5 = SumContT5 + Cells[(i-1)*49+45][k]
			SumD1 = SumD1 + Cells[(i-1)*49+5][k]
			SumD2 = SumD2 + Cells[(i-1)*49+11][k]
			SumD3 = SumD3 + Cells[(i-1)*49+19][k]
			SumD4 = SumD4 + Cells[(i-1)*49+27][k]
			SumD5 = SumD5 + Cells[(i-1)*49+35][k]
			SumD6 = SumD6 + Cells[(i-1)*49+43][k]
			
		# tseek
		if SumContT1 > 0:
			if Cells[(i-1)*49+13][3] == 1:
				Cells_plus[(i-1)*49][3] = 1
			else:
				L = 4
				while L>0 and L<cols:
					if Cells[(i-1)*49+13][L] == 1:
						Cells_plus[(i-1)*49][3] = TimInt * (Cells[(i-1)*49+48][L]-1)
						L = 0
					else:
						L = L+1
		else:
			Cells_plus[(i-1)*49][3] = 0
			
		if SumContT2 > 0:
			if Cells[(i-1)*49+21][3] == 1:
				Cells_plus[(i-1)*49+8][3] = 1
			else:
				L = 4
				while L>0 and L<cols:
					if Cells[(i-1)*49+21][L] == 1:
						Cells_plus[(i-1)*49+8][3] = TimInt * (Cells[(i-1)*49+48][L]-1)
						L = 0
					else:
						L = L+1
		else:
			Cells_plus[(i-1)*49+8][3] = 0
			
		if SumContT3 > 0:
			if Cells[(i-1)*49+29][3] == 1:
				Cells_plus[(i-1)*49+16][3] = 1
			else:
				L = 4
				while L>0 and L<cols:
					if Cells[(i-1)*49+29][L] == 1:
						Cells_plus[(i-1)*49+16][3] = TimInt * (Cells[(i-1)*49+48][L]-1)
						L = 0
					else:
						L = L+1
		else:
			Cells_plus[(i-1)*49+16][3] = 0
			
		if SumContT4 > 0:
			if Cells[(i-1)*49+37][3] == 1:
				Cells_plus[(i-1)*49+24][3] = 1
			else:
				L = 4
				while L>0 and L<cols:
					if Cells[(i-1)*49+37][L] == 1:
						Cells_plus[(i-1)*49+24][3] = TimInt * (Cells[(i-1)*49+48][L]-1)
						L = 0
					else:
						L = L+1
		else:
			Cells_plus[(i-1)*49+24][3] = 0
			
		if SumContT5 > 0:
			if Cells[(i-1)*49+45][3] == 1:
				Cells_plus[(i-1)*49+32][3] = 1
			else:
				L = 4
				while L>0 and L<cols:
					if Cells[(i-1)*49+45][L] == 1:
						Cells_plus[(i-1)*49+32][3] = TimInt * (Cells[(i-1)*49+48][L]-1)
						L = 0
					else:
						L = L+1
		else:
			Cells_plus[(i-1)*49+32][3] = 0
			
			
		# tEffDeath
		
		if SumD1 > 0:
			L = 4
			while L>0 and L<cols:
				if Cells[(i-1)*49+5][L] == 1:
					Cells_plus[(i-1)*49][4] = TimInt*(Cells[(i-1)*49+48][L]-1)
					L = 0
				else:
					L = L+1
		else:
			Cells_plus[(i-1)*49][4] = -1
			
		# Absolute time of death
		
		if SumD2 > 0:
			L = 3
			while L>0 and L<cols:
				if Cells[(i-1)*49+11][L] == 1:
					Cells_plus[(i-1)*49][5] = TimInt*(Cells[(i-1)*49+48][L]-1)
					L = 0
				else:
					L = L+1
		else:
			Cells_plus[(i-1)*49][5] = -1
			
			
		if SumD3 > 0:
			L = 3
			while L>0 and L<cols:
				if Cells[(i-1)*49+19][L] == 1:
					Cells_plus[(i-1)*49+8][5] = TimInt*(Cells[(i-1)*49+48][L]-1)
					L = 0
				else:
					L = L+1
		else:
			Cells_plus[(i-1)*49+8][5] = -1
			
			
		if SumD4 > 0:
			L = 3
			while L>0 and L<cols:
				if Cells[(i-1)*49+27][L] == 1:
					Cells_plus[(i-1)*49+16][5] = TimInt*(Cells[(i-1)*49+48][L]-1)
					L = 0
				else:
					L = L+1
		else:
			Cells_plus[(i-1)*49+16][5] = -1
			

		if SumD5 > 0:
			L = 3
			while L>0 and L<cols:
				if Cells[(i-1)*49+35][L] == 1:
					Cells_plus[(i-1)*49+24][5] = TimInt*(Cells[(i-1)*49+48][L]-1)
					L = 0
				else:
					L = L+1
		else:
			Cells_plus[(i-1)*49+24][5] = -1
			
			
		if SumD6 > 0:
			L = 3
			while L>0 and L<cols:
				if Cells[(i-1)*49+43][L] == 1:
					Cells_plus[(i-1)*49+32][5] = TimInt*(Cells[(i-1)*49+48][L]-1)
					L = 0
				else:
					L = L+1
		else:
			Cells_plus[(i-1)*49+32][5] = -1
			
			
			
		# tDeath: Check if absolute time of death >= tseek
		if Cells_plus[(i-1)*49][5] >= Cells_plus[(i-1)*49][3] and Cells_plus[(i-1)*49][3] > 0:
			Cells_plus[(i-1)*49][6] = Cells_plus[(i-1)*49][5]-Cells_plus[(i-1)*49][3]
		elif Cells_plus[(i-1)*49][5] == 0:
			Cells_plus[(i-1)*49][6] = -1
		else:
			Cells_plus[(i-1)*49][6] = -2
			

		if Cells_plus[(i-1)*49+8][5] >= Cells_plus[(i-1)*49+8][3] and Cells_plus[(i-1)*49+8][3] > 0:
			Cells_plus[(i-1)*49+8][6] = Cells_plus[(i-1)*49+8][5]-Cells_plus[(i-1)*49+8][3]
		elif Cells_plus[(i-1)*49+8][5] == 0:
			Cells_plus[(i-1)*49+8][6] = -1
		else:
			Cells_plus[(i-1)*49+8][6] = -2
			
			
		if Cells_plus[(i-1)*49+16][5] >= Cells_plus[(i-1)*49+16][3] and Cells_plus[(i-1)*49+16][3] > 0:
			Cells_plus[(i-1)*49+16][6] = Cells_plus[(i-1)*49+16][5]-Cells_plus[(i-1)*49+16][3]
		elif Cells_plus[(i-1)*49+16][5] == 0:
			Cells_plus[(i-1)*49+16][6] = -1
		else:
			Cells_plus[(i-1)*49+16][6] = -2

			
		if Cells_plus[(i-1)*49+24][5] >= Cells_plus[(i-1)*49+24][3] and Cells_plus[(i-1)*49+24][3] > 0:
			Cells_plus[(i-1)*49+24][6] = Cells_plus[(i-1)*49+24][5]-Cells_plus[(i-1)*49+24][3]
		elif Cells_plus[(i-1)*49+24][5] == 0:
			Cells_plus[(i-1)*49+24][6] = -1
		else:
			Cells_plus[(i-1)*49+24][6] = -2
			
			
		if Cells_plus[(i-1)*49+32][5] >= Cells_plus[(i-1)*49+32][3] and Cells_plus[(i-1)*49+32][3] > 0:
			Cells_plus[(i-1)*49+32][6] = Cells_plus[(i-1)*49+32][5]-Cells_plus[(i-1)*49+32][3]
		elif Cells_plus[(i-1)*49+32][5] == 0:
			Cells_plus[(i-1)*49+32][6] = -1
		else:
			Cells_plus[(i-1)*49+32][6] = -2
			
			
		# tContact (index bug...)
		
		tCont1 = 0
		if SumContT1 >0:
			if Cells_plus[(i-1)*49][6] > 0:
				for L in range(int(3+Cells_plus[(i-1)*49][3]/TimInt), int(3+Cells_plus[(i-1)*49][5]/TimInt)):
					if Cells[(i-1)*49+13][L] ==1:
						tCont1 = tCont1+1
				Cells_plus[(i-1)*49][7] = (tCont1-1)*TimInt
			elif Cells_plus[(i-1)*49][6] == 0:
				Cells_plus[(i-1)*49][7] = TimInt/2
			elif Cells_plus[(i-1)*49][6] == -1:
				for L in range(int(3+Cells_plus[(i-1)*49][3]/TimInt), cols):
					if Cells[(i-1)*49+13][L] ==1:
						tCont1 = tCont1+1
				Cells_plus[(i-1)*49][7] = (tCont1-1)*TimInt
			else:
				Cells_plus[(i-1)*49][7] = -2
		else:
			Cells_plus[(i-1)*49][7] = -1
		
		tCont2 = 0
		if SumContT2 >0:
			if Cells_plus[(i-1)*49+8][6] > 0:
				for L in range(int(3+Cells_plus[(i-1)*49+8][3]/TimInt), int(3+Cells_plus[(i-1)*49+8][5]/TimInt)):
					if Cells[(i-1)*49+21][L] ==1:
						tCont2 = tCont2+1
				Cells_plus[(i-1)*49+8][7] = (tCont2-1)*TimInt
			elif Cells_plus[(i-1)*49+8][6] == 0:
				Cells_plus[(i-1)*49+8][7] = TimInt/2
			elif Cells_plus[(i-1)*49+8][6] == -1:
				for L in range(int(3+Cells_plus[(i-1)*49+8][3]/TimInt), cols):
					if Cells[(i-1)*49+21][L] ==1:
						tCont2 = tCont2+1
				Cells_plus[(i-1)*49+8][7] = (tCont2-1)*TimInt
			else:
				Cells_plus[(i-1)*49+8][7] = -2
		else:
			Cells_plus[(i-1)*49+8][7] = -1
		
		tCont3 = 0
		if SumContT3 >0:
			if Cells_plus[(i-1)*49+16][6] > 0:
				for L in range(int(3+Cells_plus[(i-1)*49+16][3]/TimInt), int(3+Cells_plus[(i-1)*49+16][5]/TimInt)):
					if Cells[(i-1)*49+29][L] ==1:
						tCont3 = tCont3+1
				Cells_plus[(i-1)*49+16][7] = (tCont3-1)*TimInt
			elif Cells_plus[(i-1)*49+16][6] == 0:
				Cells_plus[(i-1)*49+16][7] = TimInt/2
			elif Cells_plus[(i-1)*49+16][6] == -1:
				for L in range(int(3+Cells_plus[(i-1)*49+16][3]/TimInt), cols):
					if Cells[(i-1)*49+29][L] ==1:
						tCont3 = tCont3+1
				Cells_plus[(i-1)*49+16][7] = (tCont3-1)*TimInt
			else:
				Cells_plus[(i-1)*49+16][7] = -2
		else:
			Cells_plus[(i-1)*49+16][7] = -1
		
		tCont4 = 0
		if SumContT4 >0:
			if Cells_plus[(i-1)*49+24][6] > 0:
				for L in range(int(3+Cells_plus[(i-1)*49+24][3]/TimInt), int(3+Cells_plus[(i-1)*49+24][5]/TimInt)):
					if Cells[(i-1)*49+37][L] ==1:
						tCont4 = tCont4+1
				Cells_plus[(i-1)*49+24][7] = (tCont4-1)*TimInt
			elif Cells_plus[(i-1)*49+24][6] == 0:
				Cells_plus[(i-1)*49+24][7] = TimInt/2
			elif Cells_plus[(i-1)*49+24][6] == -1:
				for L in range(int(3+Cells_plus[(i-1)*49+24][3]/TimInt), cols):
					if Cells[(i-1)*49+37][L] ==1:
						tCont4 = tCont4+1
				Cells_plus[(i-1)*49+24][7] = (tCont4-1)*TimInt
			else:
				Cells_plus[(i-1)*49+24][7] = -2
		else:
			Cells_plus[(i-1)*49+24][7] = -1
		
		tCont5 = 0
		if SumContT5 >0:
			if Cells_plus[(i-1)*49+32][6] > 0:
				for L in range(int(3+Cells_plus[(i-1)*49+32][3]/TimInt), int(3+Cells_plus[(i-1)*49+32][5]/TimInt)):
					if Cells[(i-1)*49+45][L] ==1:
						tCont5 = tCont5+1
				Cells_plus[(i-1)*49+32][7] = (tCont5-1)*TimInt
			elif Cells_plus[(i-1)*49+32][6] == 0:
				Cells_plus[(i-1)*49+32][7] = TimInt/2
			elif Cells_plus[(i-1)*49+32][6] == -1:
				for L in range(int(3+Cells_plus[(i-1)*49+32][3]/TimInt), cols):
					if Cells[(i-1)*49+45][L] ==1:
						tCont5 = tCont5+1
				Cells_plus[(i-1)*49+32][7] = (tCont5-1)*TimInt
			else:
				Cells_plus[(i-1)*49+32][7] = -2
		else:
			Cells_plus[(i-1)*49+32][7] = -1
		
		
		
		# Effector Features

		SumMotNo = 0
		CountMotNo = 0
		SumMotCont = 0
		CountMotCont = 0
		SumARNo = 0
		CountARNo = 0
		SumARCont = 0
		CountARCont = 0
		
		if Cells_plus[(i-1)*49][4]/TimInt >0:
			for k in range(3,int(Cells_plus[(i-1)*49][4]/TimInt+3+1)):
				if (Cells[(i - 1) * 49 + 13][k] + Cells[(i - 1) * 49 + 21][k] + Cells[(i - 1) * 49 + 29][k] + Cells[(i - 1) * 49 + 37][k] + Cells[(i - 1) * 49 + 45][k]) == 0:
					if Cells[(i-1)*49+3][k] > 0:
						SumMotNo = SumMotNo + Cells[(i-1)*49+3][k]
						CountMotNo = CountMotNo+1
					if Cells[(i-1)*49+2][k] > 0:
						SumARNo = SumARNo + Cells[(i-1)*49+2][k]
						CountARNo = CountARNo+1
				else:
					if Cells[(i-1)*49+3][k] > 0:
						SumMotCont = SumMotCont + Cells[(i-1)*49+3][k]
						CountMotCont = CountMotCont+1
					if Cells[(i-1)*49+2][k] > 0:
						SumARCont = SumARCont + Cells[(i-1)*49+2][k]
						CountARCont = CountARCont+1
		else:
			for k in range(3,cols):
				if (Cells[(i - 1) * 49 + 13][k] + Cells[(i - 1) * 49 + 21][k] + Cells[(i - 1) * 49 + 29][k] + Cells[(i - 1) * 49 + 37][k] + Cells[(i - 1) * 49 + 45][k]) == 0:
					if Cells[(i-1)*49+3][k] > 0:
						SumMotNo = SumMotNo + Cells[(i-1)*49+3][k]
						CountMotNo = CountMotNo+1
					if Cells[(i-1)*49+2][k] > 0:
						SumARNo = SumARNo + Cells[(i-1)*49+2][k]
						CountARNo = CountARNo+1
				else:
					if Cells[(i-1)*49+3][k] > 0:
						SumMotCont = SumMotCont + Cells[(i-1)*49+3][k]
						CountMotCont = CountMotCont+1
					if Cells[(i-1)*49+2][k] > 0:
						SumARCont = SumARCont + Cells[(i-1)*49+2][k]
						CountARCont = CountARCont+1
						
		
		# Minimum Five Time Points for average
		
		if CountMotNo > 4:
			Cells_plus[(i-1)*49][8] = Pix*SumMotNo/(CountMotNo+1)
		else:
			Cells_plus[(i-1)*49][8] = 0
			
		if CountMotCont > 4:
			Cells_plus[(i-1)*49][9] = Pix*SumMotCont/(CountMotCont+1)
		else:
			Cells_plus[(i-1)*49][9] = 0
			
		if CountARNo > 4:
			Cells_plus[(i-1)*49][10] = SumARNo/(CountARNo+1)
		else:
			Cells_plus[(i-1)*49][10] = 0
			
		if CountARNo > 4:
			Cells_plus[(i-1)*49][11] = SumARCont/(CountARCont+1)
		else:
			Cells_plus[(i-1)*49][11] = 0
			
		# Identifying Target 1
		
		if Tar1sum > -40000:
			Cells_plus[(i-1)*49+6][1] = 1
		else:
			Cells_plus[(i-1)*49+6][1] = 0
			
		# Identifying Target 2
		
		if Tar2sum > -40000:
			Cells_plus[(i-1)*49+14][1] = 1
		else:
			Cells_plus[(i-1)*49+14][1] = 0
			
		# Identifying Target 3
		
		if Tar3sum > -40000:
			Cells_plus[(i-1)*49+22][1] = 1
		else:
			Cells_plus[(i-1)*49+22][1] = 0
			
		# Identifying Target 4
		
		if Tar4sum > -40000:
			Cells_plus[(i-1)*49+30][1] = 1
		else:
			Cells_plus[(i-1)*49+30][1] = 0
			
		# Identifying Target 5
		
		if Tar5sum > -40000:
			Cells_plus[(i-1)*49+38][1] = 1
		else:
			Cells_plus[(i-1)*49+38][1] = 0
			
			
		# Total Targets
		Tar = Cells_plus[(i - 1) * 49 + 6][1] + Cells_plus[(i - 1) * 49 + 14][1] + Cells_plus[(i - 1) * 49 + 22][1] + Cells_plus[(i - 1) * 49 + 30][1] + Cells_plus[(i - 1) * 49 + 38][1]
		
		for j in range(0,49):
			
			# Generating UIDs
			Cells_UID[(i-1)*49+j] = int(Cells[(i-1)*49+j][0]*10000+Cells[(i-1)*49+j][1]*100+Cells[(i-1)*49+j][2])
			
			# Writing total targets
			Cells_plus[(i-1)*49+j][2] = Tar

			# Identifying Effectors
			if Effsum > -40000:
				Cells_plus[(i-1)*49+j][0] = 1
			else:
				Cells_plus[(i-1)*49+j][0] = 0


		# Single target features
		
		SumMotNo = 0
		CountMotNo = 0
		SumMotCont = 0
		CountMotCont = 0
		SumARNo = 0
		CountARNo = 0
		SumARCont = 0
		CountARCont = 0
		
		if Cells_plus[(i-1)*49][5]/TimInt > 0:
			for k in range(3, int(Cells_plus[(i-1)*49][5]/TimInt+3)):
				if Cells[(i-1)*49+13][k] == 0:
					if Cells[(i-1)*49+9][k] > 0:
						SumMotNo = SumMotNo + Cells[(i-1)*49+9][k]
						CountMotNo = CountMotNo + 1
					if Cells[(i-1)*49+8][k] > 0:
						SumARNo = SumARNo + Cells[(i-1)*49+8][k]
						CountARNo = CountARNo +1
				else:
					if Cells[(i-1)*49+9][k] > 0:
						SumMotCont = SumMotCont + Cells[(i-1)*49+9][k]
						CountMotCont = CountMotCont + 1
					if Cells[(i-1)*49+8][k] > 0:
						SumARCont = SumARCont + Cells[(i-1)*49+8][k]
						CountARCont = CountARCont +1
		else:
			for k in range(3,cols):
				if Cells[(i-1)*49+13][k] == 0:
					if Cells[(i-1)*49+9][k] > 0:
						SumMotNo = SumMotNo + Cells[(i-1)*49+9][k]
						CountMotNo = CountMotNo + 1
					if Cells[(i-1)*49+8][k] > 0:
						SumARNo = SumARNo + Cells[(i-1)*49+8][k]
						CountARNo = CountARNo +1
				else:
					if Cells[(i-1)*49+9][k] > 0:
						SumMotCont = SumMotCont + Cells[(i-1)*49+9][k]
						CountMotCont = CountMotCont + 1
					if Cells[(i-1)*49+8][k] > 0:
						SumARCont = SumARCont + Cells[(i-1)*49+8][k]
						CountARCont = CountARCont +1
						
		# minimum five time points for average
		
		if CountMotNo > 4:
			Cells_plus[(i-1)*49][12] = Pix*SumMotNo/CountMotNo
		else:
			Cells_plus[(i-1)*49][12] = 0
			
		if CountMotCont >4:
			Cells_plus[(i-1)*49][13] = Pix*SumMotCont/CountMotCont
		else:
			Cells_plus[(i-1)*49][13] = 0
			
		if CountARNo > 4:
			Cells_plus[(i-1)*49][14] = SumARNo/CountARNo
		else:
			Cells_plus[(i-1)*49][14] = 0
			
		if CountARCont > 4:
			Cells_plus[(i-1)*49][15] = SumARCont/CountARCont
		else:
			Cells_plus[(i-1)*49][15] = 0
			
			
			
		# E:T ratios and killing summary
		if Cells_plus[(i-1)*49][0] == 1:
			if Cells_plus[(i-1)*49][2] ==1:
				if Cells_plus[(i-1)*49][6] >= 0:
					Kill_1_1 = Kill_1_1 +1
				else:
					Dead_1_0 = Dead_1_0 +1
					if Cells_plus[(i-1)*49][3]>0:
						Kill_1_0 = Kill_1_0 + 1
			elif Cells_plus[(i-1)*49][2] == 2:
				if Cells_plus[(i-1)*49][6] >= 0 and Cells_plus[(i-1)*49+8][6] >= 0:
					Kill_2_2 = Kill_2_2 + 1
				elif Cells_plus[(i-1)*49][6] == -1 and Cells_plus[(i-1)*49+8][6] >= 0:
					Dead_2_1 = Dead_2_1 + 1
					if Cells_plus[(i-1)*49][3] > 0:
						Kill_2_1 = Kill_2_1 + 1
				elif Cells_plus[(i-1)*49][6] >= 0 and Cells_plus[(i-1)*49+8][6] == -1:
					Dead_2_1 = Dead_2_1 + 1
					if Cells_plus[(i-1)*49+8][3] > 0:
						Kill_2_1 = Kill_2_1 + 1
				else:
					Dead_2_0 = Dead_2_0 + 1
					if Cells_plus[(i-1)*49+8][3] > 0 and Cells_plus[(i-1)*49][3] > 0:
						Kill_2_0 = Kill_2_0 + 1
			elif Cells_plus[(i-1)*49][2] == 3:
				if Cells_plus[(i-1)*49][6] >= 0 and Cells_plus[(i-1)*49+8][6] >=0 and Cells_plus[(i-1)*49+16][6] >= 0:
					Kill_3_3 = Kill_3_3 + 1
				elif Cells_plus[(i-1)*49][6] >=0 and Cells_plus[(i-1)*49+8][6] >= 0 and Cells_plus[(i-1)*49+16][6] == -1:
					Dead_3_2 = Dead_3_2 + 1
					if Cells_plus[(i-1)*49+16][3] > 0:
						Kill_3_2 = Kill_3_2 + 1
				elif Cells_plus[(i-1)*49][6] >=0 and Cells_plus[(i-1)*49+8][6] == -1 and Cells_plus[(i-1)*49+16][6] >= 0:
					Dead_3_2 = Dead_3_2 + 1
					if Cells_plus[(i-1)*49+8][3] > 0:
						Kill_3_2 = Kill_3_2 + 1
				elif Cells_plus[(i-1)*49][6] == -1 and Cells_plus[(i-1)*49+8][6] >= 0 and Cells_plus[(i-1)*49+16][6] >= 0:
					Dead_3_2 = Dead_3_2 + 1
					if Cells_plus[(i-1)*49][3] > 0:
						Kill_3_2 = Kill_3_2 + 1
				elif Cells_plus[(i-1)*49][6] >=0 and Cells_plus[(i-1)*49+8][6] == -1 and Cells_plus[(i-1)*49+16][6] == -1:
					Dead_3_1 = Dead_3_1 + 1
					if Cells_plus[(i-1)*49+8][3] > 0 and Cells_plus[(i-1)*49+16][3] > 0:
						Kill_3_1 = Kill_3_1 + 1
				elif Cells_plus[(i-1)*49][6] == -1 and Cells_plus[(i-1)*49+8][6] == -1 and Cells_plus[(i-1)*49+16][6] >= 0:
					Dead_3_1 = Dead_3_1 + 1
					if Cells_plus[(i-1)*49][3] > 0 and Cells_plus[(i-1)*49+8][3] > 0:
						Kill_3_1 = Kill_3_1 + 1
				elif Cells_plus[(i-1)*49][6] == -1 and Cells_plus[(i-1)*49+8][6] >= 0 and Cells_plus[(i-1)*49+16][6] == -1:
					Dead_3_1 = Dead_3_1 + 1
					if Cells_plus[(i-1)*49][3] > 0 and Cells_plus[(i-1)*49+16][3] > 0:
						Kill_3_1 = Kill_3_1 + 1
				elif Cells_plus[(i-1)*49][6] == -1 and Cells_plus[(i-1)*49+8][6] == -1 and Cells_plus[(i-1)*49+16][6] == -1:
					Dead_3_0 = Dead_3_0 + 1
					if Cells_plus[(i-1)*49][3] > 0 and Cells_plus[(i-1)*49+8][3] > 0 and Cells_plus[(i-1)*49+16][3] > 0:
						Kill_3_0 = Kill_3_0 + 1

	# Donut Plot Table Writing out, ET Summary Table Writing out

	# The Results are stored in several variables, Cells_UID, Cells, Cells_plus
	# And The results will be written to Cells_donut, Cells_0E1T, Cells_1E0T, Cells_1E1T, Cells_1E2T, Cells_1E3T, and Cells_Master

	# feature_root_path = 'C:\\Users\\Hengyang\\Desktop\\TIMING 1.0\\result\\'
	feature_root_path = path + 'features/3_TIMING_Profile/'
	### 1. Writing Donut Table  --->  Current output is not correct

	Donut_Header = ["0 killed", "1 killied", "2 killed", "3 killed", "0 dead", "1 dead", "2 dead"]

	head_temp = '\t'.join(Donut_Header) + '\n'

	line1_list = [str(Kill_1_0), str(Kill_1_1), " ", " ", str(Dead_1_0), str(Kill_1_1), " ", " "]
	line1_temp = '\t'.join(line1_list) + '\n'

	line2_list = [str(Kill_2_0), str(Kill_2_1), str(Kill_2_2), " ", str(Dead_2_0), str(Dead_2_1), str(Kill_2_2), " "]
	line2_temp = '\t'.join(line2_list) + '\n'

	line3_list = [str(Kill_3_0), str(Kill_3_1), str(Kill_3_2), str(Kill_3_3), str(Dead_3_0), str(Dead_3_1), str(Dead_3_2), str(Kill_3_3)]
	line3_temp = '\t'.join(line3_list) + '\n'

	donut_file_name = os.getenv("HOME") + '/donut_table.txt'

	target = donut_file_name

	f = open(target,'w')
	f.writelines(head_temp)
	f.writelines(line1_temp)
	f.writelines(line2_temp)
	f.writelines(line3_temp)
	f.close()


	### 2. Writing Cells_0E1T

	filename_0E1T = os.getenv("HOME") + '/Table_0E1T.txt'
	f = open(filename_0E1T,'w')

	Header_0E1T = ["UID", "dWell No Cont (um)", "AR No Cont", "eEffDeath"]
	Header_temp = '\t'.join(Header_0E1T) + '\n'
	f.writelines(Header_temp)

	for i in range(1, wells+1):
		temp = []
		if Cells_plus[(i-1)*49][2] == 1:
			if Cells_plus[(i-1)*49][0] == 0:
				temp.append(str(Cells_UID[(i-1)*49]))
				temp.append(str(Cells_plus[(i-1)*49][12]))
				temp.append(str(Cells_plus[(i-1)*49][14]))
				temp.append(str(Cells_plus[(i-1)*49][5]))
				temp = '\t'.join(temp) + '\n'
				f.writelines(temp)

	f.close()


	### 3. Writing Cells_1E0T

	filename_1E0T = os.getenv("HOME") + '/Table_1E0T.txt'
	f = open(filename_1E0T,'w')

	Header_1E0T = ["UID", "dWell No Cont (um)", "AR No Cont", "eEffDeath"]
	Header_temp = '\t'.join(Header_1E0T) + '\n'
	f.writelines(Header_temp)

	for i in range(1, wells+1):
		temp = []
		if Cells_plus[(i-1)*49][2] == 0:
			if Cells_plus[(i-1)*49][0] == 1:
				temp.append(str(Cells_UID[(i-1)*49]))
				temp.append(str(Cells_plus[(i-1)*49][8]))
				temp.append(str(Cells_plus[(i-1)*49][10]))
				temp.append(str(Cells_plus[(i-1)*49][4]))
				temp = '\t'.join(temp) + '\n'
				f.writelines(temp)

	f.close()


	### 4. Writing Cells_1E1T

	filename_1E1T = os.getenv("HOME") + '/Table_1E1T.txt'
	f = open(filename_1E1T,'w')

	Header_1E1T = ["UID", "tSeek", "tDeath", "tContact", "Eff dWell No Cont (um)", "Eff dWell Cont (um)", "Eff AR No Cont", "Eff AR Cont", "tEffDeath", "Tar dWell No cont (um)", "Tar dWell Cont (um)", "Tar AR No cont", "Tar AR cont"]
	Header_temp = '\t'.join(Header_1E1T) + '\n'
	f.writelines(Header_temp)

	for i in range(1, wells+1):
		temp = []
		if Cells_plus[(i-1)*49][2] == 1:
			if Cells_plus[(i-1)*49][0] == 1:
				temp.append(str(Cells_UID[(i-1)*49]))
				temp.append(str(Cells_plus[(i-1)*49][3]))
				temp.append(str(Cells_plus[(i-1)*49][6]))
				temp.append(str(Cells_plus[(i-1)*49][7]))
				temp.append(str(Cells_plus[(i-1)*49][8]))
				temp.append(str(Cells_plus[(i-1)*49][9]))
				temp.append(str(Cells_plus[(i-1)*49][10]))
				temp.append(str(Cells_plus[(i-1)*49][11]))
				temp.append(str(Cells_plus[(i-1)*49][4]))
				temp.append(str(Cells_plus[(i-1)*49][12]))
				temp.append(str(Cells_plus[(i-1)*49][13]))
				temp.append(str(Cells_plus[(i-1)*49][14]))
				temp.append(str(Cells_plus[(i-1)*49][15]))
				temp = '\t'.join(temp) + '\n'
				f.writelines(temp)

	f.close()


	### 5. Writing Cells_1E2T

	filename_1E2T = os.getenv("HOME") + '/Table_1E2T.txt'
	f = open(filename_1E2T,'w')

	Header_1E2T = ["UID", "tSeek1", "tDeath1", "tContact1", "tSeek2", "tDeath2", "tContact2", "dWell No Cont(um)", "dWell Cont (um)", "AR No Cont", "AR Cont", "tEffDeath"]
	Header_temp = '\t'.join(Header_1E2T) + '\n'
	f.writelines(Header_temp)

	for i in range(1, wells+1):
		temp = []
		if Cells_plus[(i-1)*49][2] == 2:
			if Cells_plus[(i-1)*49][0] == 1:
				temp.append(str(Cells_UID[(i-1)*49]))
				temp.append(str(Cells_plus[(i-1)*49][3]))
				temp.append(str(Cells_plus[(i-1)*49][6]))
				temp.append(str(Cells_plus[(i-1)*49][7]))
				temp.append(str(Cells_plus[(i-1)*49+8][3]))
				temp.append(str(Cells_plus[(i-1)*49+8][6]))
				temp.append(str(Cells_plus[(i-1)*49+8][7]))
				temp.append(str(Cells_plus[(i-1)*49][8]))
				temp.append(str(Cells_plus[(i-1)*49][9]))
				temp.append(str(Cells_plus[(i-1)*49][10]))
				temp.append(str(Cells_plus[(i-1)*49][11]))
				temp.append(str(Cells_plus[(i-1)*49][4]))
				temp = '\t'.join(temp) + '\n'
				f.writelines(temp)

	f.close()


	### 6. Writing Cells_1E3T

	filename_1E3T = os.getenv("HOME") + '/Table_1E3T.txt'
	f = open(filename_1E3T,'w')

	Header_1E3T = ["UID", "tSeek1", "tDeath1", "tContact1", "tSeek2", "tDeath2", "tContact2", "tSeek3", "tDeath3", "tContact3", "dWell No Cont(um)", "dWell Cont (um)", "AR No Cont", "AR Cont", "tEffDeath"]
	Header_temp = '\t'.join(Header_1E3T) + '\n'
	f.writelines(Header_temp)

	for i in range(1, wells+1):
		temp = []
		if Cells_plus[(i-1)*49][2] == 3:
			if Cells_plus[(i-1)*49][0] == 1:
				temp.append(str(Cells_UID[(i-1)*49]))
				temp.append(str(Cells_plus[(i-1)*49][3]))
				temp.append(str(Cells_plus[(i-1)*49][6]))
				temp.append(str(Cells_plus[(i-1)*49][7]))
				temp.append(str(Cells_plus[(i-1)*49+8][3]))
				temp.append(str(Cells_plus[(i-1)*49+8][6]))
				temp.append(str(Cells_plus[(i-1)*49+8][7]))
				temp.append(str(Cells_plus[(i-1)*49+16][3]))
				temp.append(str(Cells_plus[(i-1)*49+16][6]))
				temp.append(str(Cells_plus[(i-1)*49+16][7]))
				temp.append(str(Cells_plus[(i-1)*49][8]))
				temp.append(str(Cells_plus[(i-1)*49][9]))
				temp.append(str(Cells_plus[(i-1)*49][10]))
				temp.append(str(Cells_plus[(i-1)*49][11]))
				temp.append(str(Cells_plus[(i-1)*49][4]))
				temp = '\t'.join(temp) + '\n'
				f.writelines(temp)

	f.close()
	
	print "Profiling Done!"



