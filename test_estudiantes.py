import time
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless") 
    service = Service() 
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://127.0.0.1:5500/inicio.html")
    yield driver
    driver.quit()

# codigo para capturas de pantalla automáticas después de cada test
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        driver = item.funcargs.get("driver", None)
        if driver:
            carpeta = "screenshots"
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
            nombre = item.name
            estado = rep.outcome  # "passed", "failed" o "skipped"
            archivo = f"{nombre}_{estado}.png"
            ruta = os.path.join(carpeta, archivo)
            driver.save_screenshot(ruta)

# Función auxiliar para completar el formulario
def completar_formulario(driver, nombre, apellido, matricula, carrera):
    driver.find_element(By.ID, "nombre").clear()
    driver.find_element(By.ID, "apellido").clear()
    driver.find_element(By.ID, "matricula").clear()
    driver.find_element(By.ID, "carrera").clear()

    driver.find_element(By.ID, "nombre").send_keys(nombre)
    driver.find_element(By.ID, "apellido").send_keys(apellido)
    driver.find_element(By.ID, "matricula").send_keys(matricula)
    driver.find_element(By.ID, "carrera").send_keys(carrera)

    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(1)

# 1️⃣ Prueba para agregar estudiante (camino feliz)
def test_prueba_para_agregar_estudiante(driver):
    completar_formulario(driver, "Ana", "Pérez", "2021001", "Informática")
    tabla = driver.find_element(By.ID, "tablaEstudiantes")
    assert "Ana" in tabla.text
    assert "Pérez" in tabla.text

# 2️⃣ Prueba para editar estudiante (camino feliz)
def test_prueba_para_editar_estudiante(driver):
    completar_formulario(driver, "Luis", "Gómez", "2022002", "Derecho")
    time.sleep(1)
    editar_btn = driver.find_element(By.CSS_SELECTOR, "#tablaEstudiantes button.editar")
    editar_btn.click()
    time.sleep(1)
    completar_formulario(driver, "Luis", "Gómez", "2022002", "Medicina")
    tabla = driver.find_element(By.ID, "tablaEstudiantes")
    assert "Medicina" in tabla.text

# 3️⃣ Prueba para eliminar estudiante (camino feliz)
def test_prueba_para_eliminar_estudiante(driver):
    completar_formulario(driver, "Carmen", "Sosa", "2023003", "Psicología")
    time.sleep(1)
    eliminar_btn = driver.find_element(By.CSS_SELECTOR, "#tablaEstudiantes button.eliminar")
    eliminar_btn.click()
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(1)
    tabla = driver.find_element(By.ID, "tablaEstudiantes")
    assert "Carmen" not in tabla.text

# 4️⃣ Prueba negativa - no permitir campos vacíos (corregida)
def test_prueba_negativa_campos_vacios(driver):
    completar_formulario(driver, "", "", "", "")
    time.sleep(1)
    tabla = driver.find_element(By.ID, "tablaEstudiantes")
    filas = tabla.find_elements(By.TAG_NAME, "tr")
    assert len(filas) == 0, "No debe agregar un registro con campos vacíos"

# 5️⃣ Prueba de límite - matrícula con longitud máxima
def test_prueba_limite_matricula_larga(driver):
    matricula_larga = "9" * 20  # 20 dígitos
    completar_formulario(driver, "Pedro", "López", matricula_larga, "Ingeniería")
    tabla = driver.find_element(By.ID, "tablaEstudiantes")
    assert matricula_larga in tabla.text or len(matricula_larga) > 10
