from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response

import json
import time
import redis
import viziocontroller

def redis_connect():
	try:
		redis_connection = redis.StrictRedis(
			host="127.0.0.1" ,
			port="6379" ,
			db=1 ,
			#password=ConfigDataBase.self[ 'redis' ][ 'password' ]
			)
		return redis_connection
	except Exception as e:
		return False

def get_tv_config_from_redis():
	try:
		redis_connection = redis_connect()
		tv_config = redis_connection.get( "CONFIG.VIZIO_TV_CONTROLLER_SERVER" )
		tv_config = json.loads( tv_config )
		tv_config = tv_config["tv"]
		return tv_config
	except Exception as e:
		print( e )
		return False

tv_blueprint = Blueprint( 'tv_blueprint' , url_prefix='/tv' )

@tv_blueprint.route( '/' )
def commands_root( request ):
	return response.text( "you are at the /tv url\n" )

@tv_blueprint.route( "/get/ip" , methods=[ "GET" ] )
def get_ip( request ):
	result = { "message": "failed" , "ip": None }
	try:
		redis_connection = redis_connect()
		config = redis_connection.get( "CONFIG.VIZIO_TV_CONTROLLER_SERVER" )
		config = json.loads( config )
		tv_config = config["tv"]
		tv = viziocontroller.VizioController( tv_config )
		if tv.ip:
			result["message"] = "success"
			result["ip"] = tv.ip
			config["tv"]["ip"] = tv.ip
			redis_connection.set( "CONFIG.VIZIO_TV_CONTROLLER_SERVER" , json.dumps( config ) )
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/volume/get" , methods=[ "GET" ] )
def volume_get( request ):
	result = { "message": "failed" , "volume": None }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		result["volume"] = tv.api.get_volume()
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/volume/up" , methods=[ "GET" ] )
def volume_up( request ):
	result = { "message": "failed" , "volume": None }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		tv.api.volume_up()
		result["volume"] = tv.api.get_volume()
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/volume/down" , methods=[ "GET" ] )
def volume_down( request ):
	result = { "message": "failed" , "volume": None }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		tv.api.volume_up()
		result["volume"] = tv.api.get_volume()
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/volume/mute/off" , methods=[ "GET" ] )
def volume_mute_off( request ):
	result = { "message": "failed" , "volume": None }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		tv.api.set_audio_setting( "mute" , "Off" )
		muted = tv.api.get_setting( "audio" , "mute" )
		result["volume"] = tv.api.get_volume()
		muted = muted["ITEMS"][0]["VALUE"]
		if muted == "On":
			muted = True
		elif muted == "Off":
			muted = False
		else:
			muted = "unknown"
		result["muted"] = muted
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/volume/mute/on" , methods=[ "GET" ] )
def volume_mute_on( request ):
	result = { "message": "failed" , "volume": None }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		tv.api.set_audio_setting( "mute" , "On" )
		muted = tv.api.get_setting( "audio" , "mute" )
		result["volume"] = tv.api.get_volume()
		muted = muted["ITEMS"][0]["VALUE"]
		if muted == "On":
			muted = True
		elif muted == "Off":
			muted = False
		else:
			muted = "unknown"
		result["muted"] = muted
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/input/get/current" , methods=[ "GET" ] )
def input_get_current( request ):
	result = { "message": "failed" }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		current_input = tv.api.get_current_input()
		result["current_input"] = current_input["name"]
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/input/get/available" , methods=[ "GET" ] )
def input_get_available( request ):
	result = { "message": "failed" }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		available_inputs = tv.api.get_available_inputs()
		available_inputs = [ x["name"] for x in available_inputs ]
		result["available_inputs"] = available_inputs
		current_input = tv.api.get_current_input()
		result["current_input"] = current_input["name"]
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/input/set" , methods=[ "GET" ] )
def input_get_available( request ):
	result = { "message": "failed" }
	try:
		input_name = request.args.get( "name" )
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		tv.api.set_input( input_name )
		current_input = tv.api.get_current_input()
		result["current_input"] = current_input["name"]
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/input/cycle" , methods=[ "GET" ] )
def input_get_available( request ):
	result = { "message": "failed" }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		tv.api.cycle_input()
		time.sleep( 1 )
		tv.api.cycle_input()
		current_input = tv.api.get_current_input()
		result["current_input"] = current_input["name"]
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )


@tv_blueprint.route( "/power/get" , methods=[ "GET" ] )
def volume_mute_on( request ):
	result = { "message": "failed" , "power_state": None }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		result["power_state"] = tv.api.get_power_state()
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/power/off" , methods=[ "GET" ] )
def volume_mute_on( request ):
	result = { "message": "failed" , "power_state": None }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		tv.api.power_off()
		result["power_state"] = tv.api.get_power_state()
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )

@tv_blueprint.route( "/power/on" , methods=[ "GET" ] )
def volume_mute_on( request ):
	result = { "message": "failed" , "power_state": None }
	try:
		tv_config = get_tv_config_from_redis()
		tv = viziocontroller.VizioController( tv_config )
		tv.api.power_on()
		result["power_state"] = tv.api.get_power_state()
		result["message"] = "success"
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json_result( result )


# Needs /set/position?track_id=asdf&position=2134
# @tv_blueprint.route( "/set/position" , methods=[ "GET" ] )
# def set_position( request ):
# 	result = { "message": "failed" , "status": None , "metadata": None }
# 	try:
# 		track_id = request.args.get( "track_id" )
# 		if track_id == None:
# 			raise Exception( "no track_id in request.args" )
# 		if position == None:
# 			raise Exception( "no position in request.args" )

# 		spotify_dbus_controller = SpotifyDBusController()
# 		spotify_dbus_controller.set_position( track_id , position )
# 		time.sleep( .5 )
# 		result["status"] = spotify_dbus_controller.get_playback_status()
# 		result["message"] = "success"
# 		result["metadata"] = spotify_dbus_controller.get_metadata()
# 	except Exception as e:
# 		print( e )
# 		result["error"] = str( e )
# 	return json_result( result )


# @tv_blueprint.route( "/set/shuffle/status/<status>" , methods=[ "GET" ] )
# def get_loop_status( request ):
# 	result = { "message": "failed" , "status": None , "metadata": None }
# 	try:
# 		spotify_dbus_controller = SpotifyDBusController()
# 		spotify_dbus_controller.set_shuffle_status( status )
# 		result["status"] = spotify_dbus_controller.get_playback_status()
# 		result["metadata"] = spotify_dbus_controller.get_metadata()
# 	except Exception as e:
# 		print( e )
# 		result["error"] = str( e )
# 	return json_result( result )