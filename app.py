from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)


def connect_db():
    caminho = os.path.join(os.path.dirname(__file__), 'instance', 'vida_plus.db')
    return sqlite3.connect(caminho)

def row_to_dict(row, keys):
    return dict(zip(keys, row)) if row else None



# ----------------- PACIENTES -----------------

# Criar paciente
@app.route('/pacientes', methods=['POST'])
def criar_paciente():
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO paciente (nome, cpf, endereco, telefone, email) VALUES (?, ?, ?, ?, ?)",
                   (data['nome'], data['cpf'], data['endereco'], data['telefone'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Paciente cadastrado com sucesso!"}), 201

# Listar todos os pacientes
@app.route('/pacientes', methods=['GET'])
def listar_pacientes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paciente")
    pacientes = cursor.fetchall()
    conn.close()
    return jsonify(pacientes), 200

# Listar paciente individualmente
@app.route('/pacientes/<int:id>', methods=['GET'])
def listar_paciente(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paciente WHERE id = ?", (id,))
    paciente = cursor.fetchone()
    conn.close()
    if paciente:
        return jsonify(paciente), 200
    else:
        return jsonify({"mensagem": "Paciente não encontrado"}), 404

# Atualizar paciente
@app.route('/pacientes/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE paciente
        SET nome = ?, cpf = ?, endereco = ?, telefone = ?, email = ?
        WHERE id = ?
    """, (data['nome'], data['cpf'], data['endereco'], data['telefone'], data['email'], id))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Paciente atualizado com sucesso!"}), 200

# Deletar paciente
@app.route('/pacientes/<int:id>', methods=['DELETE'])
def deletar_paciente(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM paciente WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Paciente deletado com sucesso!"}), 200

# ----------------- MÉDICOS   -----------------

# Criar médico
@app.route('/medicos', methods=['POST'])
def criar_medico():
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO medico (nome, crm, especialidade, telefone, email) VALUES (?, ?, ?, ?, ?)",
                   (data['nome'], data['crm'], data['especialidade'], data['telefone'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Médico cadastrado com sucesso!"}), 201

# Listar todos os médicos
@app.route('/medicos', methods=['GET'])
def listar_medicos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medico")
    medicos = cursor.fetchall()
    conn.close()
    return jsonify(medicos), 200

# Listar médico individualmente
@app.route('/medicos/<int:id>', methods=['GET'])
def listar_medico(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medico WHERE id = ?", (id,))
    medico = cursor.fetchone()
    conn.close()
    if medico:
        return jsonify(medico), 200
    else:
        return jsonify({"mensagem": "Médico não encontrado"}), 404

# Atualizar médico
@app.route('/medicos/<int:id>', methods=['PUT'])
def atualizar_medico(id):
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE medico
        SET nome = ?, crm = ?, especialidade = ?, telefone = ?, email = ?
        WHERE id = ?
    """, (data['nome'], data['crm'], data['especialidade'], data['telefone'], data['email'], id))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Médico atualizado com sucesso!"}), 200

# Deletar médico
@app.route('/medicos/<int:id>', methods=['DELETE'])
def deletar_medico(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medico WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Médico deletado com sucesso!"}), 200


# ----------------- ENFERMEIROS -----------------

@app.route('/enfermeiros', methods=['POST'])
def criar_enfermeiro():
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO enfermeiro (nome, crm, especialidade, telefone, email, turno) VALUES (?, ?, ?, ?, ?, ?)",
        (data['nome'], data['crm'], data['especialidade'], data['telefone'], data['email'], data['turno']))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Enfermeiro cadastrado com sucesso!"}), 201


@app.route('/enfermeiros', methods=['GET'])
def listar_enfermeiros():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enfermeiro")
    enfermeiros = cursor.fetchall()
    conn.close()

    # Se não houver enfermeiros cadastrados
    if not enfermeiros:
        return jsonify({"mensagem": "Nenhum enfermeiro encontrado"}), 404

    # Retornar todos os enfermeiros em formato JSON
    lista_enfermeiros = []
    for enfermeiro in enfermeiros:
        lista_enfermeiros.append({
            "id": enfermeiro[0],
            "nome": enfermeiro[1],
            "crm": enfermeiro[2],
            "especialidade": enfermeiro[3],
            "telefone": enfermeiro[4],
            "email": enfermeiro[5],
            "turno": enfermeiro[6]
        })

    return jsonify(lista_enfermeiros), 200


@app.route('/enfermeiros/<int:id>', methods=['GET'])
def listar_enfermeiro(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enfermeiro WHERE id = ?", (id,))
    enfermeiro = cursor.fetchone()
    conn.close()

    # Se o enfermeiro com o ID especificado não existir
    if not enfermeiro:
        return jsonify({"mensagem": "Enfermeiro não encontrado"}), 404

    # Retornar o enfermeiro em formato JSON
    return jsonify({
        "id": enfermeiro[0],
        "nome": enfermeiro[1],
        "crm": enfermeiro[2],
        "especialidade": enfermeiro[3],
        "telefone": enfermeiro[4],
        "email": enfermeiro[5],
        "turno": enfermeiro[6]
    }), 200


@app.route('/enfermeiros/<int:id>', methods=['PUT'])
def atualizar_enfermeiro(id):
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE enfermeiro SET nome = ?, crm = ?, especialidade = ?, telefone = ?, email = ?, turno = ? WHERE id = ?",
        (data['nome'], data['crm'], data['especialidade'], data['telefone'], data['email'], data['turno'], id))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Enfermeiro atualizado com sucesso!"}), 200


@app.route('/enfermeiros/<int:id>', methods=['DELETE'])
def deletar_enfermeiro(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enfermeiro WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Enfermeiro deletado com sucesso!"}), 200

# ----------------- TÉCNICOS -----------------
@app.route('/tecnicos', methods=['POST'])
def criar_tecnico():
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tecnico (nome, especialidade) VALUES (?, ?)",
                   (data['nome'], data['especialidade']))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Técnico cadastrado com sucesso!"}), 201


@app.route('/tecnicos', methods=['GET'])
def listar_tecnicos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tecnico")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row, ['id', 'nome', 'especialidade']) for row in rows]), 200


@app.route('/tecnicos/<int:id>', methods=['PUT'])
def atualizar_tecnico(id):
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tecnico SET nome = ?, especialidade = ? WHERE id = ?",
                   (data['nome'], data['especialidade'], id))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Técnico atualizado com sucesso!"})


@app.route('/tecnicos/<int:id>', methods=['DELETE'])
def deletar_tecnico(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tecnico WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Técnico deletado com sucesso!"})



# ----------------- CONSULTAS -----------------
# POST - Criar consulta
@app.route('/consultas', methods=['POST'])
def criar_consulta():
    dados = request.get_json()
    paciente_id = dados.get('paciente_id')
    medico_id = dados.get('medico_id')
    data_consulta = dados.get('data_consulta')
    tipo_consulta = dados.get('tipo_consulta')
    local = dados.get('local')
    status = dados.get('status')

    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO consulta (paciente_id, medico_id, data_consulta, tipo_consulta, local, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (paciente_id, medico_id, data_consulta, tipo_consulta, local, status))
    conn.commit()
    conn.close()

    return jsonify({'mensagem': 'Consulta criada com sucesso!'}), 201

# GET - Listar todas as consultas
@app.route('/consultas', methods=['GET'])
def listar_consultas():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consulta")
    consulta = cursor.fetchall()
    conn.close()
    return jsonify(consulta), 200

    lista_consultas = []
    for consulta in consultas:
        lista_consultas.append({
            'id': consulta[0],
            'paciente_id': consulta[1],
            'medico_id': consulta[2],
            'data_consulta': consulta[3],
            'tipo_consulta': consulta[4],
            'local': consulta[5],
            'status': consulta[6]
        })

    return jsonify(lista_consultas)

# GET - Consulta individual
@app.route('/consultas/<int:id>', methods=['GET'])
def obter_consulta(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM consulta WHERE id=?', (id,))
    consulta = cursor.fetchall()
    conn.close()
    return jsonify(consulta), 200


    if not consulta:
        return jsonify({'mensagem': 'Consulta não encontrada'}), 404
    else:
        return jsonify({
            'id': consulta[0],
            'paciente_id': consulta[1],
            'medico_id': consulta[2],
            'data_consulta': consulta[3],
            'tipo_consulta': consulta[4],
            'local': consulta[5],
            'status': consulta[6]
        })


# PUT - Atualizar consulta
@app.route('/consultas/<int:id>', methods=['PUT'])
def atualizar_consulta(id):
    dados = request.get_json()
    paciente_id = dados.get('paciente_id')
    medico_id = dados.get('medico_id')
    data_consulta = dados.get('data_consulta')
    tipo_consulta = dados.get('tipo_consulta')
    local = dados.get('local')
    status = dados.get('status')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE consulta
        SET paciente_id=?, medico_id=?, data_consulta=?, tipo_consulta=?, local=?, status=?
        WHERE id=?
    ''', (paciente_id, medico_id, data_consulta, tipo_consulta, local, status, id))
    conn.commit()
    conn.close()

    return jsonify({'mensagem': 'Consulta atualizada com sucesso!'})

# DELETE - Remover consulta
@app.route('/consultas/<int:id>', methods=['DELETE'])
def deletar_consulta(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM consulta WHERE id=?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'mensagem': 'Consulta removida com sucesso!'})



# ----------------- PRONTUÁRIOS -----------------
# POST - Criar prontuário

@app.route('/prontuarios', methods=['POST'])
def criar_prontuario():
    data = request.get_json()  # Aqui é "data"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prontuario (paciente_id, medico_id, data_prontuario, descricao, responsavel, anexos)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data['paciente_id'], data['medico_id'], data['data_prontuario'],
          data['descricao'], data['responsavel'], data['anexos']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Prontuário criado com sucesso!'}), 201

# GET - Listar todos os prontuários
@app.route('/prontuarios', methods=['GET'])
def listar_prontuarios():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prontuario")
    prontuarios = cursor.fetchall()
    conn.close()
    return jsonify(prontuarios)

# GET - Obter prontuário por ID
@app.route('/prontuarios/<int:id>', methods=['GET'])
def obter_prontuario(id):
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prontuario WHERE id = ?", (id,))
    prontuario = cursor.fetchone()
    conn.close()
    if prontuario:
        return jsonify(prontuarios)
    return jsonify({'mensagem': 'Prontuário não encontrado'}), 404

# PUT - Atualizar prontuário
@app.route('/prontuarios/<int:id>', methods=['PUT'])
def atualizar_prontuario(id):
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE prontuario SET
            paciente_id = ?,
            medico_id = ?,
            data_prontuario = ?,
            descricao = ?,
            responsavel = ?,
            anexos = ?
        WHERE id = ?
    """, (
        data['paciente_id'],
        data['medico_id'],
        data['data_prontuario'],
        data['descricao'],
        data['responsavel'],
        data['anexos'],
        id
    ))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Prontuário atualizado com sucesso'})

# DELETE - Remover prontuário
@app.route('/prontuarios/<int:id>', methods=['DELETE'])
def deletar_prontuario(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prontuario WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Prontuário excluído com sucesso'})

# ----------------- EXAMES -----------------
# LISTAR TODOS OS EXAMES
@app.route('/exames', methods=['POST'])
def criar_exame():
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO exame (paciente_id, tipo_exame, data_exame, resultado, responsavel, local, anexos)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data['paciente_id'], data['tipo_exame'], data['data_exame'],
        data['resultado'], data['responsavel'], data['local'], data['anexos']
    ))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Exame criado com sucesso'}), 201

@app.route('/exames', methods=['GET'])
def listar_exames():
    data = request.get_json()  # Aqui é "data"
    conn = connect_db()
    cursor = conn.cursor()
    exames = conn.execute('SELECT * FROM exame').fetchall()
    conn.close()
    return jsonify([dict(x) for x in exames])

# OBTER EXAME INDIVIDUAL
@app.route('/exames/<int:id>', methods=['GET'])
def obter_exame(id):
    data = request.get_json()  # Aqui é "data"
    conn = connect_db()
    cursor = conn.cursor()
    exame = conn.execute('SELECT * FROM exame WHERE id = ?', (id,)).fetchone()
    conn.close()
    if exame is None:
        return jsonify({'erro': 'Exame não encontrado'}), 404
    return jsonify(dict(exame))

# ATUALIZAR EXAME
@app.route('/exames/<int:id>', methods=['PUT'])
def atualizar_exame(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE exame SET paciente_id = ?, tipo_exame = ?, data_exame = ?, 
        resultado = ?, responsavel = ?, local = ?, anexos = ? WHERE id = ?
    """, (
        data['paciente_id'], data['tipo_exame'], data['data_exame'],
        data['resultado'], data['responsavel'], data['local'], data['anexos'], id
    ))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Exame atualizado com sucesso'})

# DELETAR EXAME
@app.route('/exames/<int:id>', methods=['DELETE'])
def deletar_exame(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM exame WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Exame excluído com sucesso'})

# ----------------- TELEMEDICINA -----------------
@app.route('/telemedicina', methods=['POST'])
def criar_telemedicina():
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO telemedicina (paciente_id, medico_id, data_chamada, link_chamada) VALUES (?, ?, ?, ?)",
                   (data['paciente_id'], data['medico_id'], data['data_chamada'], data['link_chamada']))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Chamada de telemedicina cadastrada!"}), 201


@app.route('/telemedicina', methods=['GET'])
def listar_telemedicina():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM telemedicina")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row, ['id', 'paciente_id', 'medico_id', 'data_chamada', 'link_chamada']) for row in rows]), 200


# ----------------- PRESCRIÇÕES -----------------
@app.route('/prescricoes', methods=['POST'])
def criar_prescricao():
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prescricao (consulta_id, medicamento, dosagem) VALUES (?, ?, ?)",
                   (data['consulta_id'], data['medicamento'], data['dosagem']))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Prescrição cadastrada com sucesso!"}), 201


@app.route('/prescricoes', methods=['GET'])
def listar_prescricoes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prescricao")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row, ['id', 'consulta_id', 'medicamento', 'dosagem']) for row in rows]), 200


if __name__ == '__main__':
    app.run(debug=True)
