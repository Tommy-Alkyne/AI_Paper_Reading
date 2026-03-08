
import os
import glob
import re

text = r"""
\cite{afraDirectNumericalSimulation2020, aidunDynamicsParticleSedimentation2003, akikiPairwiseinteractionExtendedPointparticle2017, alhasanLatticeBoltzmannLatticespringSimulations2018, amirideloueiNonNewtonianParticulateFlow2016, ardekaniNumericalStudySedimentation2016, barbeauHighorderMovingImmersed2024, batchelorSedimentationDiluteDispersion1972, caoSimulatingInteractionsTwo2015, chenEfficientFrameworkParticlefluid2020, chenLatticeBoltzmannStudy2025, chenMultidirectForcingImmersed2025, dashTwoSpheresSedimentation2015, dongMagneticFieldEffect2024, doostmohammadiInteractionPairParticles2013, EffectsChannelWidth2023a, esmaeeliDirectNumericalSimulations1998, fengDirectSimulationInitial1994, fernandesParticlelevelSimulationMagnetorheological2023, fornariSedimentationFinitesizeSpheres2016, fornariSettlingFinitesizeParticles2019, fortesNonlinearMechanicsFluidization1987, generousAssessmentInfluenceInteraction2025, ghannamOscillatoryMotionTwo2024a, ghoshNumericalSimulationsParticle2015, ghoshStudyDraftingKissing2020, glowinskiDistributedLagrangeMultiplier1997, guoGuoTaoEffectRelativePosition2024, huiEffectDensityDifference2025, jahanbakhshSiltMotionSimulation2014, karimnejadCouplingImmersedBoundary2023, laiSignedDistanceField2023, leiStudyMigrationDeposition2017, liaoSimulationsTwoSedimentinginteracting2015, liIBMLBMDEMStudyTwoParticle2022, liLatticeBoltzmannSimulation2024, liuLatticeBoltzmannSimulation2019, LiuSanWeiJuXingCaoDaoZhongKeLiChenJiangDeShuZhiMoNi2011, liuSimulatingParticleSedimentation2020, liuThreedimensionalSedimentationPatterns2023, luoImprovedDirectforcingImmersed2019, majlesaraFullyResolvedNumerical2021, maoAnisotropicLatticeBoltzmann2024, maoLatticeBoltzmannModel2024, markusImmersedBoundaryMethod2005, moricheClusteringLowaspectratioOblate2023, nagataSimpleCollisionAlgorithm2020, ngNumericalComputationFluid2021, nieInteractionTwoUnequal2021, nieSimulationSedimentationTwo2020, panghalStudyGravitationalSedimentation2024, panNumericalStudyTwo2017, patankarNewFormulationDistributed1999, perrinExplicitFinitedifferenceScheme2006, puEffectsChannelWidth2023, punchAnomalousDescentIntruders2025a, qiLatticeBoltzmannSimulationsParticles1999, rauschenbergerDirectNumericalSimulation2015, rauschenbergerParallelizedMethodDirect2015, rouhanitazangiSimulationParticlesSettling2021, safaIntegratingThermalconcentrationSmoothed2020, shajahanInertialEffectsSedimenting2023, sharmaCoupledDistributedLagrange2022, singhDistributedLagrangeMultiplier2003, strackThreedimensionalImmersedBoundary2007, stromDetailedSimulationsEffect2015, suSimulationVerificationParticle2023, taoDistributionFunctionCorrectionbased2021, taoNumericalStudyDrag2022, taoSharpInterfaceImmersed2022, tsurutaDevelopmentPARISPHEREParticlebased2019, verjusChaoticSedimentationParticle2016b, vowinckelSettlingCohesiveSediment2019, walayatFullyResolvedSimulations2019, wangCoupledPolygonalDEMLBM2021, wangDraftingKissingTumbling2014, wangInstabilityTreatmentsCoupled2020, wangInstabilityTreatmentsCoupled2020a, wangNumericalCalculationParticlefluidparticle2021, wangResearchCavitationBubble2024, wuDynamicsDualparticlesSettling1998, xiaComputationalModellingGas2024, xiaoImprovedMPSDEMNumerical2022, xiaParticleresolvedHeatparticlefluidCoupling2024, xieNovelHybridCFDDEM2023, yangEnhancedFullyResolved2024, yangLatticeBoltzmannSimulation2016, yangNoniterativeDirectForcing2015, yangSharpInterfaceDirect2014, youDirectNumericalSimulation2008, youNumericalInvestigationFreely2020, zaidiDirectNumericalSimulation2014a, zhangDirectNumericalSimulation2020, zhangDraftingKissingTumbling2023, zhangEfficientDiscreteElement2017, zhangInvestigationDraftingkissingtumblingMovement2025, zhangNumericalStudyParticle2018, zhangThreedimensionalDynamicsPair2021, ZhangXiaoJieLiuGuOuHeChuanReZuoYongXiaLiangKeLiTuoYiJieChuFanGunYunDongYanJiu2025, zhaoMetaballImagingDiscreteElement}"""

citations = re.findall(r'\\cite\{([^}]*)\}', text)
keys = [key.strip() for cit in citations for key in cit.split(',')]
print(keys)

# 假设这是你之前提取的cite键列表（从模型的输出中解析得到）
cite_keys = keys

# 获取当前目录下所有PDF文件
all_pdf_files = glob.glob("./files/*.pdf")

# 过滤出还未被重命名的PDF文件（即不是以cite key命名的）
# Cite key格式都以小写字母开头，例如 afraDirectNumericalSimulation2020
pdf_files = []
renamed_files = set()

for pdf_path in all_pdf_files:
    pdf_name = os.path.basename(pdf_path).replace('.pdf', '')
    # 检查是否已经被重命名（以某个cite key命名的）
    is_renamed = False
    for cite in cite_keys:
        if pdf_name == cite:
            is_renamed = True
            renamed_files.add(cite)
            break
    if not is_renamed:
        pdf_files.append(pdf_path)

def extract_cite_components(cite):
    """
    从cite key中提取组件：作者、标题前三个词和年份
    格式: authorTitleWord1TitleWord2TitleWord3Year[Optional_letter]
    例: afraDirectNumericalSimulation2020
    或: verjusChaoticSedimentationParticle2016b
    """
    # 提取年份（末尾4位数字，可能后跟字母）
    year_match = re.search(r'(\d{4})[a-z]?$', cite)
    if not year_match:
        return None
    year = year_match.group(1)
    
    # 提取作者部分（开头的连续小写字母）
    author_match = re.match(r'^([a-z]+)', cite)
    if not author_match:
        return None
    author = author_match.group(1)
    
    # 找到年份在cite中的位置（可能没有后缀字母）
    year_idx = cite.find(year)
    if year_idx == -1:
        return None
    
    # 提取标题部分（作者和年份之间的部分）
    title_part = cite[len(author):year_idx]
    
    # 驼峰分割
    spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', title_part)
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', spaced)
    
    title_words = [w.lower() for w in spaced.split() if w][:3]
    
    return {
        'author': author,
        'title_words': title_words,
        'year': year,
        'full_cite': cite
    }

def extract_pdf_components(pdf_name):
    """
    从PDF文件名中提取组件
    格式: Author Name - Year - Title...pdf 或 Year - Title...pdf
    例: Afra 等 - 2020 - Direct numerical simulation...pdf
    """
    # 移除.pdf扩展名
    name_without_ext = pdf_name.replace('.pdf', '')
    
    # 尝试提取年份
    year_match = re.search(r'(\d{4})', name_without_ext)
    if not year_match:
        return None  # 如果没有年份，跳过这个文件
    year = year_match.group(1)
    year_idx = name_without_ext.find(year)
    
    # 提取作者名（年份前面的部分，通常在第一个" - "之前）
    dash_positions = [m.start() for m in re.finditer(' - ', name_without_ext)]
    author_part = ""
    
    # 检查年份是否在最开头（如 "2005 - Title..."）
    if year_idx == 0:
        author_part = ""  # 没有作者信息
    elif dash_positions:
        author_part = name_without_ext[:dash_positions[0]].strip()
    else:
        author_part = name_without_ext[:year_idx].strip()
    
    # 提取标题（年份后面的部分）
    title_start = year_idx + len(year)
    if title_start < len(name_without_ext):
        remaining = name_without_ext[title_start:]
        dash_idx = remaining.find(' - ')
        if dash_idx != -1:
            title_part = remaining[dash_idx + 3:].strip()
        else:
            title_part = remaining.strip().lstrip('- ')
    else:
        title_part = ""
    
    # 提取标题中的单词，只取字母部分（移除连字符等）
    # 将连字符和其他特殊字符替换为空格，然后分割
    title_part = re.sub(r'[^a-zA-Z\s]', ' ', title_part)
    # 移除常见介词和冠词，只保留实际内容词
    stopwords = {'in', 'a', 'an', 'the', 'of', 'and', 'or', 'with', 'for', 'by', 'as', 'at', 'to', 'from'}
    title_words_raw = title_part.split()
    title_words = [w.lower() for w in title_words_raw if w.lower() not in stopwords][:3]
    
    # 如果移除stopwords后没有足够的词，使用原始的
    if len(title_words) < 2:
        title_words = [w.lower() for w in title_words_raw][:3]
    
    return {
        'author_part': author_part.lower(),
        'title_words': title_words,
        'year': year,
        'pdf_name': pdf_name
    }

# 第一轮：年份+作者+标题的严格匹配
print("第一轮：严格匹配（年份+作者+标题）...\n")

for cite in cite_keys:
    cite_components = extract_cite_components(cite)
    if not cite_components:
        continue
    
    candidates = []
    for pdf_file in pdf_files:
        pdf_name = os.path.basename(pdf_file)
        pdf_components = extract_pdf_components(pdf_name)
        if not pdf_components:
            continue
        
        # 年份匹配
        year_match = cite_components['year'] == pdf_components['year']
        
        # 作者匹配
        if not pdf_components['author_part']:
            author_match = True
        else:
            author_match = (
                cite_components['author'][0].lower() == pdf_components['author_part'][0] or
                cite_components['author'].lower() in pdf_components['author_part']
            )
        
        # 标题匹配
        cite_title = cite_components['title_words']
        pdf_full_title = pdf_name.lower()
        
        title_match = False
        if len(cite_title) >= 2:
            w1_lower = cite_title[0].lower()
            w2_lower = cite_title[1].lower()
            title_match = w1_lower in pdf_full_title and w2_lower in pdf_full_title
        elif len(cite_title) == 1:
            title_match = cite_title[0].lower() in pdf_full_title
        
        if year_match and author_match and title_match:
            candidates.append(pdf_file)
    
    if len(candidates) == 1:
        old_path = candidates[0]
        new_name = cite + ".pdf"
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        if os.path.exists(new_path):
            print(f"警告：目标文件名 {new_name} 已存在，跳过 {old_path}")
        else:
            os.rename(old_path, new_path)
            print(f"✓ {new_name}")
            pdf_files.remove(old_path)

# 第二轮：年份+作者的宽松匹配（不检查标题）
print("\n第二轮：宽松匹配（仅年份+作者）...\n")

for cite in cite_keys:
    cite_components = extract_cite_components(cite)
    if not cite_components:
        continue
    
    # 检查这个cite key是否已经被匹配
    target_name = cite + ".pdf"
    if os.path.exists(os.path.join("./files", target_name)):
        continue
    
    candidates = []
    for pdf_file in pdf_files:
        pdf_name = os.path.basename(pdf_file)
        pdf_components = extract_pdf_components(pdf_name)
        if not pdf_components:
            # 尝试从没有年份的PDF中提取作者和进行匹配
            name_without_ext = pdf_name.replace('.pdf', '')
            dash_idx = name_without_ext.find(' - ')
            if dash_idx != -1:
                author_part = name_without_ext[:dash_idx].lower()
                author_match = (
                    cite_components['author'][0].lower() == author_part[0] or
                    cite_components['author'].lower() in author_part
                )
            else:
                author_match = False
            
            year_match = False
        else:
            # 年份匹配
            year_match = cite_components['year'] == pdf_components['year']
            
            # 作者匹配
            if not pdf_components['author_part']:
                author_match = True
            else:
                author_match = (
                    cite_components['author'][0].lower() == pdf_components['author_part'][0] or
                    cite_components['author'].lower() in pdf_components['author_part']
                )
        
        if year_match and author_match:
            candidates.append(pdf_file)
    
    if len(candidates) == 1:
        old_path = candidates[0]
        new_name = cite + ".pdf"
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        if os.path.exists(new_path):
            print(f"警告：文件已存在: {new_name}")
        else:
            os.rename(old_path, new_path)
            print(f"✓ {new_name} (宽松匹配)")
            pdf_files.remove(old_path)
    elif len(candidates) > 1:
        print(f"⚠ 多个候选: {cite} ({len(candidates)} 个)")


print("\n第三轮：处理没有年份的cite keys...")

# 重新加载所有cite keys并找那些没有年份的
cite_keys_without_year = []
for cite in keys:
    cite_components = extract_cite_components(cite)
    if not cite_components and not re.search(r'\d{4}', cite):
        # 这是一个没有年份的cite key
        # 手动提取作者（开头的小写字母）
        author_match = re.match(r'^([a-z]+)', cite)
        if author_match:
            cite_keys_without_year.append({
                'cite': cite,
                'author': author_match.group(1),
                'title': cite[len(author_match.group(1)):]
            })

if cite_keys_without_year:
    print(f"找到 {len(cite_keys_without_year)} 个没有年份的cite keys\n")
    
    for cite_info in cite_keys_without_year:
        # 检查是否已被匹配
        target_name = cite_info['cite'] + ".pdf"
        if os.path.exists(os.path.join("./files", target_name)):
            print(f"✓ {cite_info['cite']} (已匹配)")
            continue
        
        candidates = []
        for pdf_file in pdf_files:
            pdf_name = os.path.basename(pdf_file)
            name_lower = pdf_name.lower()
            
            author_lower = cite_info['author'].lower()
            
            # 检查作者是否出现在PDF文件名中
            if author_lower not in name_lower:
                continue
            
            # 对标题进行驼峰分割
            title_part = cite_info['title']
            # 在大写前添加空格
            spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', title_part)
            title_words = [w.lower() for w in spaced.split() if w]
            
            # 检查标题中的至少首个词是否在PDF文件名中找到
            title_match = False
            if len(title_words) >= 2:
                # 前两个词都要找到
                title_match = (
                    title_words[0] in name_lower and
                    title_words[1] in name_lower
                )
            elif title_words:
                title_match = title_words[0] in name_lower
            
            if title_match:
                candidates.append(pdf_file)
        
        if len(candidates) == 1:
            old_path = candidates[0]
            new_name = cite_info['cite'] + ".pdf"
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            if os.path.exists(new_path):
                print(f"警告：{new_name} 已存在")
            else:
                os.rename(old_path, new_path)
                print(f"✓ {new_name} (无年份匹配)")
                pdf_files.remove(old_path)
        elif len(candidates) > 1:
            print(f"⚠ {cite_info['cite']}: 找到 {len(candidates)} 个候选")
        else:
            print(f"✗ {cite_info['cite']}: 未找到匹配")
renamed_count = sum(1 for f in glob.glob("./files/*.pdf") if re.match(r'^[a-z]+[A-Z].*\d{4}\.pdf$', os.path.basename(f)))
print(f"成功重命名: {renamed_count} 个文件")
print(f"待处理: {len(pdf_files)} 个文件")
print(f"总计: {len(all_pdf_files)} 个PDF文件")
print("="*60)