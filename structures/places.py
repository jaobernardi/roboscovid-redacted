from .enums import PlaceType
from .files import Messages, Config
from utils import parse_string
from random import choice
from datetime import datetime


class BulletinField:
	def __init__(self, var_name, name="", is_warning=False, final_character="", notation="", quantitative="", hs_notification=False):
		self.var_name = var_name
		self.name = name
		self.is_warning = is_warning
		self.notation = notation
		self.quantitative = quantitative
		self.hs_notification = hs_notification
		self.final_character = final_character


class Place:
	def __init__(self, name, state, font, type, field_map: list = [], **kwargs):
		self.name = name
		self.header = "header"
		self.footer = "footer"
		self.type = type
		self.state = state
		self.field_map = [
			BulletinField("cases", "Casos Confirmados", quantitative="caso(s)"),
			BulletinField("deaths", "Óbitos", quantitative="óbito(s)"),
			BulletinField("recovered", "Recuperados", quantitative="recuperado(s)"),
			BulletinField("active_cases", "Casos Ativos", quantitative="caso(s)")

		]
		self.changed = False
		self.field_map.extend(field_map)
		self.issue = datetime.now()
		self.font = font
		self.__dict__.update(kwargs)

	@property
	def flag_report_fields(self):
		if hasattr(self, "flag"):
			msg = Messages()


			time = self.issue.strftime("%d/%m/%Y às %H:%M")
			header = parse_string(msg.reports[self.header], {"name": self.name, "font": self.font})
			foot_note = parse_string(msg.reports["foot_notice"], {"foot_notice": choice(msg.reports["foot_notes"])})
			footer = parse_string(msg.reports[self.footer], {"name": self.name, "font": self.font, "time": time})
			body = f"```Bandeira Atual:``` {self.flag}\n"+(f"```Bandeira Anterior:``` {self.old_flag}\n" if hasattr(self, "old_flag") else "")
			
			config = Config()

			for warning in config.warnings:
				if "reports" in warning["display"]:
					if warning['place'][0] == self.state and (warning['place'][1] == self.name if warning['place'][1] else True):
						effective_start = datetime.strptime(warning["effective_since"], "%d/%m/%Y %H:%M")
						effective_until = datetime.strptime(warning["effective_until"], "%d/%m/%Y %H:%M")

						if datetime.now() >= effective_start and datetime.now() <= effective_until:
							foot_note = warning["message"]

			return [header, body, foot_note, footer]

	@property
	def flag_report(self):
		msg = Messages()
		return "\n".join(self.flag_report_fields)	

	@property
	def tag(self):
		return [self.state, (self.name if self.type == PlaceType.CITY else None)]
	
	@property
	def report_fields(self):
		msg = Messages()
		time = self.issue.strftime("%d/%m/%Y às %H:%M")
		header = parse_string(msg.reports[self.header], {"name": self.name, "font": self.font})
		foot_note = parse_string(msg.reports["foot_notice"], {"foot_notice": choice(msg.reports["foot_notes"])})
		footer = parse_string(msg.reports[self.footer], {"name": self.name, "font": self.font, "time": time})
		body = ""
		attrs = {i.var_name:i for i in self.field_map if i.var_name in self.__dict__}
		for attr in attrs:
			if attr in self.__dict__ and self.__dict__[attr]:
				if attrs[attr].is_warning:
					body += f"{self.__dict__[attr]}\n"
				else:
					body += f"```{attrs[attr].name}:``` _{self.__dict__[attr]}{attrs[attr].final_character}_ {attrs[attr].notation}\n"
		if not body:
			body = "\n⚠ Não foi possível coletar nenhum dado para esta região... Um aviso foi enviado para a Equipe de Desenvolvimento.\n"
		
		config = Config()

		for warning in config.warnings:
			if "reports" in warning["display"]:
				if warning['place'][0] == self.state and (warning['place'][1] == self.name if warning['place'][1] else True):
					effective_start = datetime.strptime(warning["effective_since"], "%d/%m/%Y %H:%M")
					effective_until = datetime.strptime(warning["effective_until"], "%d/%m/%Y %H:%M")

					if datetime.now() >= effective_start and datetime.now() <= effective_until:
						foot_note = parse_string(msg.reports["foot_notice"], {"foot_notice": warning["message"]})
		return [header, body, foot_note, footer]

	@property
	def no_format_report(self):
		return "\n".join(self.report_fields).replace("```", "").replace("*", "").replace("_", "")

	@property
	def report(self):
		return "\n".join(self.report_fields)

	@property
	def hs_notification_fields(self):
		msg = Messages()
		header = parse_string(msg.hs_notifications[self.header], {"name": self.name, "font": self.font})
		footer = msg.hs_notifications["footer"]
		body = ""
		attrs = {i.var_name:i for i in self.field_map if i.hs_notification and i.var_name in self.__dict__}

		for attr in attrs:
			if attrs[attr].is_warning:
				body += f"{self.__dict__[attr]}"

		for attr in attrs:
			if not attrs[attr].is_warning:
				body += f"{attrs[attr].name}:``` _{self.__dict__[attr]}{attrs[attr].final_character}_ {attrs[attr].notation}"

		if not body:
			body = "\n⚠ Não foi possível gerar nenhum aviso. Uma notificação foi enviada para a Equipe de Desenvolvimento.\n"
		return [header, body, footer]

	@property
	def hs_notification(self):
		return "\n".join(self.hs_notification_fields)

	@property
	def no_format_hs_notification(self):
		return "\n".join(self.hs_notification_fields).replace("```", "").replace("*", "").replace("_", "")


	def __add__(self, other):
		if hasattr(other, "flag"):
			self.old_flag = other.flag
		attrs = {i.var_name:i for i in self.field_map if i.var_name in self.__dict__ and i.quantitative and not i.hs_notification}
		other_attrs = {i.var_name:i for i in other.field_map if i.var_name in self.__dict__ and i.quantitative and not i.hs_notification}
		for attr in other_attrs:
			if other_attrs[attr].hs_notification:
				continue

			if attr in attrs:
				value = self.__dict__[attr]
				other_value = other.__dict__[attr]
				if isinstance(value, int) and isinstance(other_value, int) or isinstance(value, float) and isinstance(other_value, float):
					diff = value - other_value
					if diff > 0:
						self.changed = True
						attrs[attr].notation = f"*+{diff}* _{attrs[attr].quantitative} novos_"
					if diff < 0:
						self.changed = True
						attrs[attr].notation = f"*{diff}* _{attrs[attr].quantitative}_"
		return self


class Hospital(Place):
	def __init__(self, name, city, font, field_map: list=[], **kwargs):
		super().__init__(name, "", font, PlaceType.STREETBLOCK, field_map, ooter="minimal_footer", header="minimal_header", city=city, **kwargs)

	@property
	def report_fields(self):
		msg = Messages()
		time = self.issue.strftime("%d/%m/%Y às %H:%M")
		header = parse_string(msg.reports[self.header], {"name": self.name, "font": self.font})
		body = ""
		attrs = {i.var_name:i for i in self.field_map if i.var_name in self.__dict__}
		for attr in attrs:
			if attr in self.__dict__ and self.__dict__[attr]:
				if attrs[attr].is_warning:
					body += f"{self.__dict__[attr]}\n"
				else:
					body += f"```{attrs[attr].name}:``` _{self.__dict__[attr]}{attrs[attr].final_character}_ {attrs[attr].notation}\n"
		if not body:
			body = "\n⚠ Não foi possível coletar nenhum dado para esta região... Um aviso foi enviado para a Equipe de Desenvolvimento.\n"
		return [header, body]

 
class StreetBlock(Place):
	def __init__(self, name, city, font, field_map: list=[], **kwargs):
		super().__init__(name, "", font, PlaceType.STREETBLOCK, field_map, header="minimal_header", footer="minimal_footer", city=city, **kwargs)

	@property
	def report_fields(self):
		msg = Messages()
		time = self.issue.strftime("%d/%m/%Y às %H:%M")
		header = parse_string(msg.reports[self.header], {"name": self.city+", "+self.name, "font": self.font})
		foot_note = parse_string(msg.reports["foot_notice"], {"foot_notice": choice(msg.reports["foot_notes"])})
		footer = parse_string(msg.reports[self.footer], {"name": self.name, "font": self.font, "time": time})
		body = ""
		attrs = {i.var_name:i for i in self.field_map if not i.hs_notification and i.var_name in self.__dict__}
		for attr in attrs:
			if attr in self.__dict__ and self.__dict__[attr]:
				if attrs[attr].is_warning:
					body += f"{self.__dict__[attr]}\n"
				else:
					body += f"```{attrs[attr].name}:``` _{self.__dict__[attr]}{attrs[attr].final_character}_ {attrs[attr].notation}\n"
		if not body:
			body = "\n⚠ Não foi possível coletar nenhum dado para esta região... Um aviso foi enviado para a Equipe de Desenvolvimento.\n"
		return [header, body, foot_note, footer]
